import asyncio
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, AsyncGenerator, Dict, Optional
from uuid import UUID, uuid4
from loguru import logger
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import String, DateTime, ForeignKey, select, UUID as SQ_UUID, JSON
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from faststream import FastStream
from faststream.rabbit import RabbitBroker, TestRabbitBroker

logger.add(
    sink=lambda msg: print(msg, end=""),
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
    enqueue=True
)

class Base(DeclarativeBase):
    pass

class Shipment(Base):
    __tablename__ = "shipments"

    id: Mapped[UUID] = mapped_column(SQ_UUID, primary_key=True, default=uuid4)
    tracking_code: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    carrier: Mapped[str] = mapped_column(String(50), nullable=False)
    promised_delivery_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="IN_TRANSIT")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    checkpoints: Mapped[list["CheckpointLedger"]] = relationship("CheckpointLedger", back_populates="shipment", cascade="all, delete-orphan")

class CheckpointLedger(Base):
    __tablename__ = "checkpoint_ledger"

    id: Mapped[UUID] = mapped_column(SQ_UUID, primary_key=True, default=uuid4)
    shipment_id: Mapped[UUID] = mapped_column(SQ_UUID, ForeignKey("shipments.id", ondelete="CASCADE"), nullable=False)
    location_hub: Mapped[str] = mapped_column(String(100), nullable=False)
    arrival_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status_description: Mapped[str] = mapped_column(String(255), nullable=False)
    raw_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)

    shipment: Mapped["Shipment"] = relationship("Shipment", back_populates="checkpoints")

class DatabaseManager:
    def __init__(self, database_url: str) -> None:
        self._engine = create_async_engine(database_url, echo=False)
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                logger.error(f"Transaction rollback: {str(e)}")
                raise
            finally:
                await session.close()

    async def create_tables(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

class CarrierCheckpointEvent(BaseModel):
    model_config = ConfigDict(extra="allow", frozen=True)
    tracking_code: str
    location_hub: str
    status_timestamp: datetime
    status_description: str

class DelayAlertPayload(BaseModel):
    shipment_id: str
    tracking_code: str
    carrier: str
    risk_score: float
    calculated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status_description: str

class LogisticsRiskEngine:
    @staticmethod
    async def predict_delay_probability(hours_at_hub: float, carrier_historical_delay_rate: float, days_remaining: float) -> float:
        logger.info(f"AI Engine crunching metrics -> Hours At Hub: {hours_at_hub}, Carrier Base Risk: {carrier_historical_delay_rate}, Days Left: {days_remaining}")
        await asyncio.sleep(0.05)
        if days_remaining <= 1:
            return 0.89  
        return 0.25

broker = RabbitBroker()
app = FastStream(broker)

db_manager = DatabaseManager("sqlite+aiosqlite:///:memory:")
risk_engine = LogisticsRiskEngine()

@broker.subscriber("carrier.checkpoints")
async def handle_carrier_checkpoint(payload: Dict[str, Any]) -> None:
    logger.info("Event consumed from 'carrier.checkpoints' pipeline.")
    try:
        event_data = CarrierCheckpointEvent.model_validate(payload)
    except Exception as err:
        logger.error(f"Invalid payload schema. Aborting. Trace: {str(err)}")
        return

    try:
        async for session in db_manager.get_session():
            shipment_query = await session.execute(
                select(Shipment).where(Shipment.tracking_code == event_data.tracking_code)
            )
            shipment: Optional[Shipment] = shipment_query.scalar_one_or_none()

            if not shipment:
                logger.warning(f"Orphaned event: tracking code '{event_data.tracking_code}' not found in database.")
                return

            new_entry = CheckpointLedger(
                shipment_id=shipment.id,
                location_hub=event_data.location_hub,
                arrival_timestamp=event_data.status_timestamp,
                status_description=event_data.status_description,
                raw_payload=payload
            )
            session.add(new_entry)
            
            risk_score = await risk_engine.predict_delay_probability(
                hours_at_hub=12.5,
                carrier_historical_delay_rate=0.28,
                days_remaining=1.0
            )

            logger.info(f"Calculated SLA Risk Score for Package: {risk_score}")

            if risk_score >= 0.75:
                logger.warning(f"🚨 CRITICAL OVERWATCH ALERT: Risk score {risk_score} violates SLA for {shipment.tracking_code}")
                
                alert = DelayAlertPayload(
                    shipment_id=str(shipment.id),
                    tracking_code=shipment.tracking_code,
                    carrier=shipment.carrier,
                    risk_score=risk_score,
                    status_description=event_data.status_description
                )
                
                await broker.publish(alert.model_dump(mode="json"), queue="logistics.alerts.delay")
                logger.info("Downstream alert notification published successfully to 'logistics.alerts.delay'.")

    except Exception as system_fault:
        logger.error(f"Internal processing failure: {str(system_fault)}")

@broker.subscriber("logistics.alerts.delay")
async def handle_downstream_alert(payload: Dict[str, Any]) -> None:
    logger.info(f"🔔 ALERT CONSUMER ACTIVATED: Successfully received risk signal for {payload.get('tracking_code')} | Score: {payload.get('risk_score')}")

@app.after_startup
async def run_automated_simulation() -> None:
    logger.info("🚀 Starting Automated Simulation Environment...")
    await db_manager.create_tables()
    
    async with db_manager._session_factory() as session:
        mock_shipment = Shipment(
            id=uuid4(),
            tracking_code="AEGIS-QUANTUM-99",
            carrier="DHL_EXPRESS",
            promised_delivery_date=datetime.now(timezone.utc) + timedelta(days=1),
            status="IN_TRANSIT"
        )
        session.add(mock_shipment)
        await session.commit()
    logger.info("Database initialized with contract: 'AEGIS-QUANTUM-99'")

    await asyncio.sleep(1)
    logger.info("Simulating carrier transmission: incoming checkpoint radio alert...")
    
    mock_event = {
        "tracking_code": "AEGIS-QUANTUM-99",
        "location_hub": "BERLIN_LOGISTICS_HUB_A",
        "status_timestamp": datetime.now(timezone.utc).isoformat(),
        "status_description": "Package held for customs anomalies inspection"
    }
    await broker.publish(mock_event, queue="carrier.checkpoints")

async def main():
    async with TestRabbitBroker(broker):
        await app.run()

if __name__ == "__main__":
    logger.info("Initializing Headless Systems Context...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Process terminated clean by operator command.")