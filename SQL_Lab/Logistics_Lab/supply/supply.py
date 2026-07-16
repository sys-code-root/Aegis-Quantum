import asyncio
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
import logging
from typing import List, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sklearn.linear_model import LinearRegression
from sqlalchemy import String, Integer, Numeric, Date, ForeignKey, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SupplyEngine")

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sku: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    current_stock: Mapped[int] = mapped_column(Integer, nullable=False)
    lead_time_days: Mapped[int] = mapped_column(Integer, nullable=False)

class SalesHistory(Base):
    __tablename__ = "sales_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False)
    sale_date: Mapped[date] = mapped_column(Date, nullable=False)
    quantity_sold: Mapped[int] = mapped_column(Integer, nullable=False)

class DatabaseManager:
    def __init__(self, connection_string: str = "sqlite+aiosqlite:///:memory:"):
        self.engine = create_async_engine(connection_string, echo=False)
        self.session_factory = async_sessionmaker(self.engine, expire_on_commit=False)

    async def initialize_database(self) -> None:
        async with self.engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    async def seed_mock_data(self) -> None:
        async with self.session_factory() as session:
            async with session.begin():
                today = date.today()
                
                p1 = Product(sku="SKU-CHIP-X1", name="Quantum Processing Unit v1", current_stock=45, lead_time_days=5)
                p2 = Product(sku="SKU-NEURAL-LINK", name="Neural Interface Node", current_stock=12, lead_time_days=7)
                p3 = Product(sku="SKU-CYBER-CORE", name="Fusion Core Cell Block", current_stock=120, lead_time_days=3)
                session.add_all([p1, p2, p3])
                await session.flush()

                sales = []
                for i in range(30, 0, -1):
                    sale_date = today - timedelta(days=i)
                    sales.append(SalesHistory(product_id=p1.id, sale_date=sale_date, quantity_sold=np.random.randint(2, 6)))
                    sales.append(SalesHistory(product_id=p2.id, sale_date=sale_date, quantity_sold=np.random.randint(3, 8)))
                    sales.append(SalesHistory(product_id=p3.id, sale_date=sale_date, quantity_sold=np.random.randint(1, 4)))
                session.add_all(sales)

class DemandPredictor:
    @staticmethod
    def forecast_zero_stock_date(sales_df: pd.DataFrame, current_stock: int) -> Tuple[int, float]:
        if sales_df.empty or len(sales_df) < 2:
            return 0, 0.0
            
        grouped_sales = sales_df.groupby("sale_date")["quantity_sold"].sum().reset_index()
        grouped_sales["day_index"] = np.arange(len(grouped_sales))
        
        X = grouped_sales[["day_index"]]
        y = grouped_sales["quantity_sold"]
        
        model = LinearRegression()
        model.fit(X, y)
        
        avg_daily_demand = max(float(model.predict([[len(grouped_sales)]])[0]), 0.1)
        days_until_zero = int(np.ceil(current_stock / avg_daily_demand))
        
        return days_until_zero, avg_daily_demand

class PresentationDataService:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    async def fetch_inventory_status(self) -> List[dict]:
        async with self.db_manager.session_factory() as session:
            product_query = select(Product)
            product_result = await session.execute(product_query)
            products = product_result.scalars().all()
            
            inventory_reports = []
            for product in products:
                sales_query = select(SalesHistory).where(SalesHistory.product_id == product.id)
                sales_result = await session.execute(sales_query)
                sales = sales_result.scalars().all()
                
                sales_df = pd.DataFrame([{
                    "sale_date": s.sale_date, "quantity_sold": s.quantity_sold
                } for s in sales])
                
                days_left, avg_demand = DemandPredictor.forecast_zero_stock_date(sales_df, product.current_stock)
                
                reorder_point = int(np.ceil(avg_demand * product.lead_time_days))
                action_required = "HOLD"
                
                if days_left <= product.lead_time_days:
                    action_required = "CRITICAL REORDER"
                elif product.current_stock <= reorder_point:
                    action_required = "WARNING"
                    
                suggested_purchase = max(int(np.ceil(avg_demand * 30)) - product.current_stock, 0)

                inventory_reports.append({
                    "id": product.id,
                    "sku": product.sku,
                    "name": product.name,
                    "current_stock": product.current_stock,
                    "lead_time": product.lead_time_days,
                    "avg_demand": round(avg_demand, 2),
                    "days_until_zero": days_left,
                    "reorder_point": reorder_point,
                    "suggested_purchase": suggested_purchase,
                    "action_required": action_required,
                    "sales_data": sales_df
                })
            return inventory_reports

def initialize_application_state() -> None:
    if "db_manager" not in st.session_state:
        st.session_state.db_manager = DatabaseManager()
        st.session_state.data_service = PresentationDataService(st.session_state.db_manager)
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        loop.run_until_complete(st.session_state.db_manager.initialize_database())
        loop.run_until_complete(st.session_state.db_manager.seed_mock_data())

def render_dashboard() -> None:
    st.set_page_config(page_title="REORDER MATRIX", layout="wide")
    
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Share+Tech+Mono&display=swap');
            
            .stApp { 
                background-color: #0a0a0c; 
                color: #e0e0e6;
                font-family: 'Share Tech Mono', monospace;
            }
            h1, h2, h3, h4, h5, h6, .stMarkdown { 
                font-family: 'Orbitron', sans-serif; 
            }
            div[data-testid="stSidebar"] {
                background-color: #0d0d11;
                border-right: 1px solid #00f0ff;
                box-shadow: 0 0 15px rgba(0, 240, 255, 0.1);
            }
            .sidebar-title {
                color: #00f0ff;
                font-size: 1.4rem;
                font-weight: 700;
                text-shadow: 0 0 10px rgba(0, 240, 255, 0.7);
                text-align: center;
                margin-bottom: 2rem;
            }
            .cyber-card {
                background: rgba(10, 10, 12, 0.8);
                border: 1px solid #00f0ff;
                box-shadow: 0 0 15px rgba(0, 240, 255, 0.3);
                padding: 20px;
                border-radius: 6px;
                text-align: center;
                margin-bottom: 15px;
            }
            .card-critical {
                border-color: #ff0055;
                box-shadow: 0 0 15px rgba(255, 0, 85, 0.4);
            }
            .card-warning {
                border-color: #ffaa00;
                box-shadow: 0 0 15px rgba(255, 170, 0, 0.3);
            }
            .metric-val {
                font-size: 2rem;
                font-weight: bold;
                text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
            }
            .val-critical { color: #ff0055; text-shadow: 0 0 10px #ff0055; }
            .val-warning { color: #ffaa00; text-shadow: 0 0 10px #ffaa00; }
            .val-hold { color: #39ff14; text-shadow: 0 0 10px #39ff14; }
            
            .alert-banner {
                background: rgba(255, 0, 85, 0.1);
                border: 1px solid #ff0055;
                box-shadow: 0 0 10px rgba(255, 0, 85, 0.3);
                color: #ff0055;
                padding: 12px;
                border-radius: 4px;
                font-family: 'Orbitron';
                font-weight: bold;
                margin-bottom: 15px;
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)

    initialize_application_state()
    
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    reports = loop.run_until_complete(st.session_state.data_service.fetch_inventory_status())

    with st.sidebar:
        st.markdown('<div class="sidebar-title">AEGIS SUPPLY CHAIN</div>', unsafe_allow_html=True)
        st.write(f"SYSTEM OVERWATCH: ACTIVE")
        st.write(f"PREDICTIVE ENGINE: READY")

    st.title("⚡ REORDER MATRIX")
    st.markdown("---")

    critical_alerts = [r for r in reports if r["action_required"] == "CRITICAL REORDER"]
    for alert in critical_alerts:
        st.markdown(f'<div class="alert-banner">🚨 OPERATIONAL CRITICAL: RESUPPLY {alert["name"]} ({alert["sku"]}) WITHIN {alert["days_until_zero"]} DAYS</div>', unsafe_allow_html=True)

    cols = st.columns(len(reports))
    for idx, report in enumerate(reports):
        with cols[idx]:
            card_style = "cyber-card"
            val_style = "metric-val"
            if report["action_required"] == "CRITICAL REORDER":
                card_style += " card-critical"
                val_style += " val-critical"
            elif report["action_required"] == "WARNING":
                card_style += " card-warning"
                val_style += " val-warning"
            else:
                val_style += " val-hold"

            st.markdown(f"""
                <div class="{card_style}">
                    <div style="font-size:0.8rem; color:#a0a0ab;">{report["sku"]}</div>
                    <div style="font-size:1.1rem; font-weight:bold; margin-bottom:10px;">{report["name"]}</div>
                    <div style="font-size:0.75rem; color:#a0a0ab;">STOCK VOLUME</div>
                    <div class="{val_style}">{report["current_stock"]} units</div>
                    <div style="font-size:0.75rem; color:#a0a0ab; margin-top:5px;">DEPLETION VELOCITY</div>
                    <div style="font-weight:bold;">{report["days_until_zero"]} Days Left</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📊 PREDICTIVE STOCK DEPLETION CURVES")

    selected_product_name = st.selectbox("SELECT TARGET COMPONENTS FOR LOGISTICAL DECAY ANALYSIS:", [r["name"] for r in reports])
    selected_report = next(r for r in reports if r["name"] == selected_product_name)
    
    sales_df = selected_report["sales_data"]
    
    if not sales_df.empty:
        sales_df = sales_df.sort_values("sale_date").reset_index()
        
        historical_stock = []
        stock_tracker = selected_report["current_stock"] + sales_df["quantity_sold"].sum()
        
        for qty in sales_df["quantity_sold"]:
            stock_tracker -= qty
            historical_stock.append(stock_tracker)
            
        sales_df["computed_stock"] = historical_stock

        future_days = list(range(1, selected_report["days_until_zero"] + 5))
        future_dates = [date.today() + timedelta(days=d) for d in future_days]
        future_stock = [max(selected_report["current_stock"] - int(np.ceil(selected_report["avg_demand"] * d)), 0) for d in future_days]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=sales_df["sale_date"], y=sales_df["computed_stock"],
            name="Historical Ledger", line=dict(color="#00f0ff", width=3)
        ))
        fig.add_trace(go.Scatter(
            x=future_dates, y=future_stock,
            name="ML Predictive Decay", line=dict(color="#ff0055", width=3, dash="dash")
        ))
        fig.add_trace(go.Scatter(
            x=[date.today() + timedelta(days=selected_report["days_until_zero"])], y=[0],
            mode="markers", name="Exhaustion Target Point", marker=dict(color="#ffaa00", size=12, symbol="x")
        ))

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(10,10,12,1)",
            plot_bgcolor="rgba(13,13,17,1)",
            xaxis=dict(gridcolor="rgba(0, 240, 255, 0.1)", tickfont=dict(family="Orbitron", color="#00f0ff")),
            yaxis=dict(gridcolor="rgba(0, 240, 255, 0.1)", tickfont=dict(family="Share Tech Mono", color="#e0e0e6")),
            margin=dict(l=40, r=40, t=20, b=40),
            height=380
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("📡 STRATEGIC PROCUREMENT PROCUREMENT SUGGESTIONS")
    
    table_rows = ""
    for r in reports:
        badge_color = "#39ff14" if r["action_required"] == "HOLD" else ("#ffaa00" if r["action_required"] == "WARNING" else "#ff0055")
        badge_border = f"1px solid {badge_color}"
        badge_shadow = f"0 0 5px {badge_color}"
        status_badge = f'<span style="color:{badge_color}; border:{badge_border}; box-shadow:{badge_shadow}; padding:2px 6px; border-radius:3px; font-size:0.8rem; font-weight:bold;">{r["action_required"]}</span>'
        
        table_rows += f"""<tr style="border-bottom: 1px solid rgba(0, 240, 255, 0.15); background: rgba(13,13,17,0.5)">
            <td style="padding:12px; font-family:'Orbitron'; color:#00f0ff">{r["sku"]}</td>
            <td style="padding:12px; font-family:'Share Tech Mono'; color:#ffffff">{r["name"]}</td>
            <td style="padding:12px; font-family:'Share Tech Mono'; color:#e0e0e6; text-align:center;">{r["current_stock"]}</td>
            <td style="padding:12px; font-family:'Share Tech Mono'; color:#ffaa00; text-align:center;">{r["reorder_point"]}</td>
            <td style="padding:12px; font-family:'Share Tech Mono'; color:#ff0055; text-align:center; font-weight:bold;">{r["days_until_zero"]} Days</td>
            <td style="padding:12px; font-family:'Share Tech Mono'; color:#39ff14; text-align:center; font-weight:bold;">+{r["suggested_purchase"]} units</td>
            <td style="padding:12px; font-family:'Orbitron'; text-align:center;">{status_badge}</td>
        </tr>"""

    html_table = f"""<table style="width:100%; border-collapse: collapse; text-align: left;">
        <thead>
            <tr style="border-bottom: 2px solid #00f0ff; color: #00f0ff; font-family:'Orbitron'">
                <th style="padding:12px;">SKU CHIP</th>
                <th style="padding:12px;">COMPONENT NAME</th>
                <th style="padding:12px; text-align:center;">CURRENT</th>
                <th style="padding:12px; text-align:center;">MIN REORDER POINT</th>
                <th style="padding:12px; text-align:center;">TIME TO ZERO</th>
                <th style="padding:12px; text-align:center;">ORDER SUGGESTION</th>
                <th style="padding:12px; text-align:center;">SYSTEM STATUS</th>
            </tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>"""
    st.markdown(html_table, unsafe_allow_html=True)

if __name__ == "__main__":
    render_dashboard()