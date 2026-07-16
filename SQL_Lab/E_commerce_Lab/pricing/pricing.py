import enum
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from typing import AsyncGenerator

from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import String, Numeric as SQLDecimal, Integer, Boolean, DateTime, select, Enum as SAEnum
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("PricingEngine")

DATABASE_URL = "sqlite+aiosqlite:///:memory:"
GLOBAL_PRICE_FLOOR = Decimal("0.70")  
AI_SAFETY_FLOOR = Decimal("0.85")    

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

class CouponType(str, enum.Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"

class ProductModel(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    base_price: Mapped[Decimal] = mapped_column(SQLDecimal(10, 2), nullable=False)
    stock_volume: Mapped[int] = mapped_column(Integer, default=0)
    competitor_price: Mapped[Decimal] = mapped_column(SQLDecimal(10, 2), nullable=False)

class CouponModel(Base):
    __tablename__ = "coupons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    type: Mapped[CouponType] = mapped_column(SAEnum(CouponType, native_enum=False), nullable=False)
    value: Mapped[Decimal] = mapped_column(SQLDecimal(10, 2), nullable=False)
    min_purchase_value: Mapped[Decimal] = mapped_column(SQLDecimal(10, 2), default=Decimal("0.00"))
    target_region: Mapped[str | None] = mapped_column(String(2), nullable=True)
    first_purchase_only: Mapped[bool] = mapped_column(Boolean, default=False)
    excluded_categories: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

class PricingRequest(BaseModel):
    product_id: int
    user_region: str = Field(..., min_length=2, max_length=2, description="State/Region ISO code")
    is_first_purchase: bool = False
    coupon_codes: list[str] = Field(default_factory=list)

    @field_validator("user_region", mode="before")
    @classmethod
    def normalize_region(cls, v: str) -> str:
        return str(v).strip().upper() if v else v

    @field_validator("coupon_codes", mode="before")
    @classmethod
    def clean_coupon_codes(cls, v: list) -> list[str]:
        if isinstance(v, list):
            return [str(code).strip().upper() for code in v if code]
        return v

class AppliedCouponSchema(BaseModel):
    code: str
    discount_applied: Decimal

class PricingResponse(BaseModel):
    product_id: int
    base_price: Decimal
    dynamic_price: Decimal
    applied_coupons: list[AppliedCouponSchema]
    invalid_or_expired_coupons: list[str] = Field(default_factory=list)
    final_price: Decimal

class PricingEngineService:
    
    @staticmethod
    async def analyze_market_with_ai(product: ProductModel) -> Decimal:
        try:
            base = Decimal(str(product.base_price))
            competitor = Decimal(str(product.competitor_price))
            stock = product.stock_volume

            if stock < 5 and competitor > base:
                ai_modifier = Decimal("1.18")
            elif stock > 120 and competitor < base:
                ai_modifier = Decimal("0.88")
            else:
                ai_modifier = (competitor * Decimal("0.98")) / base
                
            calculated_price = base * ai_modifier
            
        except Exception as e:
            logger.error(f"AI Pricing Engine Inference anomaly: {str(e)}. Falling back to baseline price.")
            calculated_price = product.base_price
            
        safety_floor = product.base_price * AI_SAFETY_FLOOR
        return max(calculated_price, safety_floor).quantize(Decimal("0.00"))

    @classmethod
    def process_coupons(
        cls, 
        current_price: Decimal, 
        category: str, 
        request: PricingRequest, 
        coupons: list[CouponModel]
    ) -> tuple[list[AppliedCouponSchema], Decimal]:
        applied_coupons: list[AppliedCouponSchema] = []
        running_price = current_price

        sorted_coupons = sorted(coupons, key=lambda c: 0 if c.type == CouponType.PERCENTAGE else 1)

        for coupon in sorted_coupons:
            if running_price < coupon.min_purchase_value:
                continue

            if coupon.target_region and coupon.target_region != request.user_region:
                continue

            if coupon.first_purchase_only and not request.is_first_purchase:
                continue

            if coupon.excluded_categories:
                if category.lower() in [c.strip().lower() for c in coupon.excluded_categories.split(",")]:
                    continue

            if coupon.type == CouponType.PERCENTAGE:
                discount = running_price * (coupon.value / Decimal("100"))
            else:
                discount = coupon.value

            discount = min(discount, running_price)
            running_price -= discount

            applied_coupons.append(
                AppliedCouponSchema(
                    code=coupon.code, 
                    discount_applied=discount.quantize(Decimal("0.00"))
                )
            )

        return applied_coupons, running_price

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as session:
        now = datetime.now(timezone.utc)
        
        session.add_all([
            ProductModel(name="Mechanical Keyboard", category="Peripherals", base_price=Decimal("300.00"), stock_volume=3, competitor_price=Decimal("320.00")),
            ProductModel(name="Gaming Monitor 24", category="Monitors", base_price=Decimal("1200.00"), stock_volume=150, competitor_price=Decimal("1100.00"))
        ])
        
        session.add_all([
            CouponModel(code="WELCOME10", type=CouponType.PERCENTAGE, value=Decimal("10.00"), first_purchase_only=True, is_active=True, start_date=now - timedelta(days=1), end_date=now + timedelta(days=10)),
            CouponModel(code="NYDISCOUNT", type=CouponType.FIXED, value=Decimal("50.00"), target_region="NY", min_purchase_value=Decimal("200.00"), is_active=True, start_date=now - timedelta(days=1), end_date=now + timedelta(days=5)),
            CouponModel(code="PROMOEXCLUDE", type=CouponType.PERCENTAGE, value=Decimal("20.00"), excluded_categories="Peripherals", is_active=True, start_date=now - timedelta(days=2), end_date=now + timedelta(days=2)),
            CouponModel(code="CYBERPROMO", type=CouponType.PERCENTAGE, value=Decimal("30.00"), is_active=True, start_date=now - timedelta(days=10), end_date=now - timedelta(days=1)),
            CouponModel(code="INACTIVE50", type=CouponType.FIXED, value=Decimal("50.00"), is_active=False, start_date=now - timedelta(days=1), end_date=now + timedelta(days=1))
        ])
        await session.commit()
    yield
    await engine.dispose()

app = FastAPI(title="Dynamic Pricing & AI Coupon Engine API", version="2.5.0", lifespan=lifespan)

@app.post(
    "/api/v1/pricing/calculate", 
    response_model=PricingResponse, 
    status_code=status.HTTP_200_OK,
    summary="Calculates market intelligence via AI and validates corporate coupons"
)
async def calculate_pricing(request: PricingRequest, db: AsyncSession = Depends(get_db)):
    product = await db.get(ProductModel, request.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Product ID {request.product_id} not found."
        )

    valid_coupons_to_process = []
    invalid_or_expired_codes = []
    
    if request.coupon_codes:
        unique_requested_codes = set(request.coupon_codes)
        
        coupon_result = await db.execute(
            select(CouponModel).where(CouponModel.code.in_(unique_requested_codes))
        )
        found_coupons = coupon_result.scalars().all()
        found_codes_set = {c.code for c in found_coupons}
        
        for code in unique_requested_codes:
            if code not in found_codes_set:
                invalid_or_expired_codes.append(code)
                
        current_time = datetime.now(timezone.utc)
        for coupon in found_coupons:
            coupon_start = coupon.start_date.replace(tzinfo=timezone.utc) if not coupon.start_date.tzinfo else coupon.start_date
            coupon_end = coupon.end_date.replace(tzinfo=timezone.utc) if not coupon.end_date.tzinfo else coupon.end_date
            
            if not coupon.is_active or not (coupon_start <= current_time <= coupon_end):
                invalid_or_expired_codes.append(coupon.code)
            else:
                valid_coupons_to_process.append(coupon)

    dynamic_price = await PricingEngineService.analyze_market_with_ai(product)

    processed_coupons, computed_final_price = PricingEngineService.process_coupons(
        current_price=dynamic_price,
        category=product.category,
        request=request,
        coupons=valid_coupons_to_process
    )
    
    absolute_price_floor = product.base_price * GLOBAL_PRICE_FLOOR
    final_price = max(computed_final_price, absolute_price_floor)

    return PricingResponse(
        product_id=product.id,
        base_price=product.base_price,
        dynamic_price=dynamic_price,
        applied_coupons=processed_coupons,
        invalid_or_expired_coupons=invalid_or_expired_codes,
        final_price=final_price.quantize(Decimal("0.00"))
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("pricing:app", host="127.0.0.1", port=8000, reload=True)