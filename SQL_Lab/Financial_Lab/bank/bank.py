import io
import datetime
from decimal import Decimal
from contextlib import asynccontextmanager
from typing import AsyncGenerator, List, Optional, Tuple, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

import pandas as pd
from ofxparse import OfxParser
from rapidfuzz import fuzz, process
from sklearn.ensemble import IsolationForest
import numpy as np

from fastapi import FastAPI, Depends, HTTPException, status, APIRouter, UploadFile, File
from sqlalchemy import Numeric, String, Date, select, and_, Boolean, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    pass


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


class GatewayTransaction(Base):
    __tablename__ = "gateway_transactions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    fee: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False, default=Decimal("0.0000"))
    description: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, default="PENDING")


class BankTransaction(Base):
    __tablename__ = "bank_transactions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, default="PENDING")


class ReconciliationLog(Base):
    __tablename__ = "reconciliation_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    gateway_transaction_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    bank_transaction_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    match_type: Mapped[str] = mapped_column(String, nullable=False)
    confidence_score: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    anomaly_flag: Mapped[bool] = mapped_column(Boolean, default=False)


class TransactionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    date: datetime.date
    amount: Decimal = Field(..., max_digits=18, decimal_places=4)
    description: str
    status: str


class ReconciliationSummary(BaseModel):
    exact_matches: int
    fuzzy_matches: int
    anomalies_detected: int
    execution_status: str


class ReconciliationService:
    """Provides business logic and data engineering capabilities for transaction reconciliation."""

    @staticmethod
    def parse_ofx(file_content: bytes) -> List[Dict[str, Any]]:
        """Parses bank transaction data from standard OFX files."""
        ofx_buffer = io.BytesIO(file_content)
        ofx = OfxParser.parse(ofx_buffer)
        parsed_transactions = []
        
        for account in ofx.accounts:
            for tx in account.statement.transactions:
                parsed_transactions.append({
                    "id": str(tx.id),
                    "date": tx.date.date(),
                    "amount": Decimal(str(tx.amount)),
                    "description": str(tx.memo or tx.payee).strip()
                })
        return parsed_transactions

    @staticmethod
    def parse_gateway_csv(file_content: bytes) -> List[Dict[str, Any]]:
        """Parses gateway transaction records from standard CSV exports."""
        csv_buffer = io.BytesIO(file_content)
        dataframe = pd.read_csv(csv_buffer, dtype={"id": str, "description": str})
        
        dataframe["amount"] = dataframe["amount"].astype(str).apply(Decimal)
        dataframe["fee"] = dataframe["fee"].astype(str).apply(Decimal)
        dataframe["date"] = pd.to_datetime(dataframe["date"]).dt.date
        
        return dataframe.to_dict(orient="records")

    @staticmethod
    async def execute_exact_match(db: AsyncSession) -> List[Tuple[GatewayTransaction, BankTransaction]]:
        """Performs optimized batch-matching over primary indices and financial parameters via IN queries."""
        bank_stmt = select(BankTransaction).where(BankTransaction.status == "PENDING")
        bank_result = await db.execute(bank_stmt)
        bank_transactions = bank_result.scalars().all()

        if not bank_transactions:
            return []

        bank_ids = [tx.id for tx in bank_transactions]

        gateway_stmt = select(GatewayTransaction).where(
            and_(
                GatewayTransaction.id.in_(bank_ids),
                GatewayTransaction.status == "PENDING"
            )
        )
        gateway_result = await db.execute(gateway_stmt)
        gateway_transactions = gateway_result.scalars().all()

        gateway_map = {tx.id: tx for tx in gateway_transactions}
        matches = []

        for bank_tx in bank_transactions:
            if bank_tx.id in gateway_map:
                gateway_tx = gateway_map[bank_tx.id]
                if gateway_tx.amount == bank_tx.amount:
                    matches.append((gateway_tx, bank_tx))

        return matches

    @staticmethod
    async def execute_fuzzy_match(db: AsyncSession, threshold: float = 75.0) -> List[Dict[str, Any]]:
        """Executes secondary text similarity processing on unmatched pending entries."""
        gateway_stmt = select(GatewayTransaction).where(GatewayTransaction.status == "PENDING")
        bank_stmt = select(BankTransaction).where(BankTransaction.status == "PENDING")
        
        gateway_transactions = (await db.execute(gateway_stmt)).scalars().all()
        bank_transactions = (await db.execute(bank_stmt)).scalars().all()
        
        matches = []
        if not gateway_transactions or not bank_transactions:
            return matches

        bank_description_map = {tx.description: tx for tx in bank_transactions}
        bank_descriptions = list(bank_description_map.keys())

        for gateway_tx in gateway_transactions:
            extraction_result = process.extractOne(
                gateway_tx.description, 
                bank_descriptions, 
                scorer=fuzz.token_set_ratio
            )
            
            if extraction_result:
                best_match_description, score, _ = extraction_result
                if score >= threshold:
                    matched_bank_transaction = bank_description_map[best_match_description]
                    
                    if gateway_tx.amount == matched_bank_transaction.amount:
                        matches.append({
                            "gateway": gateway_tx,
                            "bank": matched_bank_transaction,
                            "score": Decimal(str(score))
                        })
                        bank_descriptions.remove(best_match_description)
                        
        return matches

    @staticmethod
    def detect_fee_anomalies(gateway_records: List[Dict[str, Any]], contamination: float = 0.05) -> List[bool]:
        """Utilizes an Isolation Forest estimator to identify irregular operational fees."""
        if not gateway_records:
            return []
            
        features = np.array([
            [float(tx["amount"]), float(tx["fee"])] 
            for tx in gateway_records
        ])
        
        isolation_forest = IsolationForest(contamination=contamination, random_state=42)
        predictions = isolation_forest.fit_predict(features)
        
        return [prediction == -1 for prediction in predictions]


router = APIRouter(prefix="/reconciliation", tags=["Reconciliation"])


@router.post("/process", response_model=ReconciliationSummary, status_code=status.HTTP_200_OK)
async def process_reconciliation(
    ofx_file: UploadFile = File(...),
    csv_file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db_session)
):
    try:
        ofx_content = await ofx_file.read()
        csv_content = await csv_file.read()
        
        bank_data = ReconciliationService.parse_ofx(ofx_content)
        gateway_data = ReconciliationService.parse_gateway_csv(csv_content)
        
        for tx in bank_data:
            db.add(BankTransaction(id=tx["id"], date=tx["date"], amount=tx["amount"], description=tx["description"]))
        for tx in gateway_data:
            db.add(GatewayTransaction(id=tx["id"], date=tx["date"], amount=tx["amount"], fee=tx["fee"], description=tx["description"]))
        
        await db.flush()

        exact_matches = await ReconciliationService.execute_exact_match(db)
        for gateway, bank in exact_matches:
            gateway.status = "RECONCILED"
            bank.status = "RECONCILED"
            db.add(ReconciliationLog(
                gateway_transaction_id=gateway.id,
                bank_transaction_id=bank.id,
                match_type="EXACT",
                confidence_score=Decimal("100.00"),
                anomaly_flag=False
            ))
        
        await db.flush()

        fuzzy_matches = await ReconciliationService.execute_fuzzy_match(db)
        for match in fuzzy_matches:
            gateway = match["gateway"]
            bank = match["bank"]
            gateway.status = "RECONCILED"
            bank.status = "RECONCILED"
            db.add(ReconciliationLog(
                gateway_transaction_id=gateway.id,
                bank_transaction_id=bank.id,
                match_type="FUZZY",
                confidence_score=match["score"],
                anomaly_flag=False
            ))

        await db.flush()

        anomalies = ReconciliationService.detect_fee_anomalies(gateway_data)
        anomaly_count = 0
        for tx, is_anomaly in zip(gateway_data, anomalies):
            if is_anomaly:
                anomaly_count += 1
                db.add(ReconciliationLog(
                    gateway_transaction_id=tx["id"],
                    bank_transaction_id=None,
                    match_type="UNMATCHED",
                    confidence_score=Decimal("0.00"),
                    anomaly_flag=True
                ))

        return ReconciliationSummary(
            exact_matches=len(exact_matches),
            fuzzy_matches=len(fuzzy_matches),
            anomalies_detected=anomaly_count,
            execution_status="SUCCESS"
        )

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal operational failure within the reconciliation engine: {str(error)}"
        )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Automated Bank Reconciliation System", lifespan=lifespan)
app.include_router(router)