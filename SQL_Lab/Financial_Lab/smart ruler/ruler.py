import asyncio
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
import logging
from typing import List, Tuple

from apscheduler.schedulers.background import BackgroundScheduler
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sqlalchemy import Column, String, Integer, Numeric, Date, DateTime, ForeignKey, select, update
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BillingEngine")

class Base(DeclarativeBase):
    pass

class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_id: Mapped[str] = mapped_column(String, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2), nullable=False)
    accumulated_fees: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2), default=Decimal("0.00"))
    status: Mapped[str] = mapped_column(String, default="PENDING")

class CommunicationLog(Base):
    __tablename__ = "communication_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    invoice_id: Mapped[int] = mapped_column(Integer, ForeignKey("invoices.id"), nullable=False)
    action_taken: Mapped[str] = mapped_column(String, nullable=False)
    dispatched_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

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
                invoices = [
                    Invoice(customer_id="CUST-101", due_date=today - timedelta(days=15), amount=Decimal("1500.00"), status="OVERDUE"),
                    Invoice(customer_id="CUST-102", due_date=today - timedelta(days=45), amount=Decimal("2800.00"), status="OVERDUE"),
                    Invoice(customer_id="CUST-103", due_date=today - timedelta(days=75), amount=Decimal("5000.00"), status="OVERDUE"),
                    Invoice(customer_id="CUST-104", due_date=today + timedelta(days=5), amount=Decimal("1200.00"), status="PENDING"),
                    Invoice(customer_id="CUST-105", due_date=today - timedelta(days=5), amount=Decimal("950.00"), status="OVERDUE"),
                    Invoice(customer_id="CUST-106", due_date=today - timedelta(days=32), amount=Decimal("4300.00"), status="OVERDUE"),
                    Invoice(customer_id="CUST-107", due_date=today - timedelta(days=12), amount=Decimal("600.00"), status="PAID")
                ]
                session.add_all(invoices)

class RiskEngine:
    def __init__(self):
        self.model = RandomForestClassifier(random_state=42)
        self._train_mock_model()

    def _train_mock_model(self) -> None:
        features = np.array([
            [15, 1500.00, 1],
            [45, 2800.00, 2],
            [75, 5000.00, 3],
            [5, 950.00, 0],
            [32, 4300.00, 2],
            [3, 500.00, 0],
            [90, 10000.00, 5]
        ])
        labels = np.array([1, 0, 0, 1, 0, 1, 0])
        self.model.fit(features, labels)

    def predict_probability(self, days_overdue: int, amount: Decimal, historical_delays: int) -> float:
        input_data = np.array([[days_overdue, float(amount), historical_delays]])
        probabilities = self.model.predict_proba(input_data)
        return float(probabilities[0][1])

class CommunicationDispatcher:
    @staticmethod
    async def dispatch_soft_reminder(invoice_id: int, customer_id: str, amount: Decimal) -> str:
        await asyncio.sleep(0.01)
        return f"Email Reminder Sent to {customer_id} for Invoice #{invoice_id} [Amount: ${amount}]"

    @staticmethod
    async def dispatch_critical_alert(invoice_id: int, customer_id: str, amount: Decimal) -> str:
        await asyncio.sleep(0.01)
        return f"Webhook Critical Escalation Triggered for {customer_id} [Total Debt: ${amount}]"

class BillingAutomationEngine:
    def __init__(self, db_manager: DatabaseManager, risk_engine: RiskEngine):
        self.db_manager = db_manager
        self.risk_engine = risk_engine
        self.fine_rate = Decimal("0.02")
        self.daily_interest_rate = Decimal("0.00033")

    async def execute_daily_billing_sweep(self) -> None:
        today = date.today()
        async with self.db_manager.session_factory() as session:
            async with session.begin():
                query = select(Invoice).where(Invoice.status == "OVERDUE")
                result = await session.execute(query)
                overdue_invoices = result.scalars().all()

                for invoice in overdue_invoices:
                    days_past_due = (today - invoice.due_date).days
                    if days_past_due <= 0:
                        continue

                    base_fine = invoice.amount * self.fine_rate
                    compounded = invoice.amount * ((Decimal("1.0") + self.daily_interest_rate) ** days_past_due)
                    calculated_fees = base_fine + (compounded - invoice.amount)
                    invoice.accumulated_fees = calculated_fees.quantize(Decimal("0.01"))

                    recovery_probability = self.risk_engine.predict_probability(
                        days_overdue=days_past_due,
                        amount=invoice.amount,
                        historical_delays=2
                    )

                    total_due = invoice.amount + invoice.accumulated_fees
                    if recovery_probability >= 0.5:
                        action = await CommunicationDispatcher.dispatch_soft_reminder(invoice.id, invoice.customer_id, total_due)
                    else:
                        action = await CommunicationDispatcher.dispatch_critical_alert(invoice.id, invoice.customer_id, total_due)

                    log_entry = CommunicationLog(invoice_id=invoice.id, action_taken=action)
                    session.add(log_entry)

class PresentationDataService:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    async def fetch_invoice_metrics(self) -> pd.DataFrame:
        async with self.db_manager.session_factory() as session:
            result = await session.execute(select(Invoice))
            invoices = result.scalars().all()
            return pd.DataFrame([{
                "id": i.id, "customer_id": i.customer_id, "due_date": i.due_date,
                "amount": float(i.amount), "accumulated_fees": float(i.accumulated_fees), "status": i.status
            } for i in invoices])

    async def fetch_communication_logs(self) -> pd.DataFrame:
        async with self.db_manager.session_factory() as session:
            result = await session.execute(select(CommunicationLog).order_by(CommunicationLog.dispatched_at.desc()))
            logs = result.scalars().all()
            return pd.DataFrame([{
                "id": l.id, "invoice_id": l.invoice_id, "action_taken": l.action_taken, "dispatched_at": l.dispatched_at
            } for l in logs])

def construct_aging_buckets(dataframe: pd.DataFrame) -> pd.DataFrame:
    if dataframe.empty:
        return pd.DataFrame(columns=["Aging Bucket", "Outstanding Balance"])
    
    today = date.today()
    dataframe["due_date"] = pd.to_datetime(dataframe["due_date"]).dt.date
    overdue_df = dataframe[dataframe["status"] == "OVERDUE"].copy()
    
    if overdue_df.empty:
        return pd.DataFrame(columns=["Aging Bucket", "Outstanding Balance"])

    overdue_df["days_past"] = overdue_df["due_date"].apply(lambda x: (today - x).days)
    overdue_df["total_debt"] = overdue_df["amount"] + overdue_df["accumulated_fees"]

    conditions = [
        (overdue_df["days_past"] <= 30),
        (overdue_df["days_past"] > 30) & (overdue_df["days_past"] <= 60),
        (overdue_df["days_past"] > 60)
    ]
    choices = ["1-30 Days", "31-60 Days", "60+ Days"]
    overdue_df["Aging Bucket"] = np.select(conditions, choices, default="Unknown")
    
    grouped = overdue_df.groupby("Aging Bucket", observed=False)["total_debt"].sum().reset_index()
    grouped.columns = ["Aging Bucket", "Outstanding Balance"]
    
    bucket_order = {bucket: i for i, bucket in enumerate(choices)}
    grouped["order"] = grouped["Aging Bucket"].map(bucket_order)
    return grouped.sort_values("order").drop(columns=["order"])

def initialize_application_state() -> None:
    if "db_manager" not in st.session_state:
            st.session_state.db_manager = DatabaseManager()
            st.session_state.risk_engine = RiskEngine()
            st.session_state.automation = BillingAutomationEngine(st.session_state.db_manager, st.session_state.risk_engine)
            st.session_state.data_service = PresentationDataService(st.session_state.db_manager)
            
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
            loop.run_until_complete(st.session_state.db_manager.initialize_database())
            loop.run_until_complete(st.session_state.db_manager.seed_mock_data())
            loop.run_until_complete(st.session_state.automation.execute_daily_billing_sweep())
            
            def run_billing_sweep_sync():
                new_loop = asyncio.new_event_loop()
                try:
                    asyncio.set_event_loop(new_loop)
                    new_loop.run_until_complete(st.session_state.automation.execute_daily_billing_sweep())
                finally:
                    new_loop.close()

            scheduler = BackgroundScheduler()
            scheduler.add_job(run_billing_sweep_sync, "interval", minutes=5)
            scheduler.start()
            st.session_state.scheduler = scheduler

def render_dashboard() -> None:
    st.set_page_config(page_title="AEGIS DunEngine v1.0", layout="wide")
    
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
                font-size: 1.6rem;
                font-weight: 700;
                text-shadow: 0 0 10px rgba(0, 240, 255, 0.7);
                margin-bottom: 2rem;
                text-align: center;
            }
            .sidebar-metric {
                background: rgba(13, 13, 17, 0.65);
                border: 1px solid #39ff14;
                padding: 10px;
                border-radius: 4px;
                box-shadow: 0 0 8px rgba(57, 255, 20, 0.2);
                margin-bottom: 10px;
            }
            .cyber-card-magenta {
                background: rgba(10, 10, 12, 0.8);
                border: 1px solid #ff0055;
                box-shadow: 0 0 15px rgba(255, 0, 85, 0.4);
                padding: 20px;
                border-radius: 6px;
                text-align: center;
            }
            .cyber-card-cyan {
                background: rgba(10, 10, 12, 0.8);
                border: 1px solid #00f0ff;
                box-shadow: 0 0 15px rgba(0, 240, 255, 0.4);
                padding: 20px;
                border-radius: 6px;
                text-align: center;
            }
            .cyber-card-green {
                background: rgba(10, 10, 12, 0.8);
                border: 1px solid #39ff14;
                box-shadow: 0 0 15px rgba(57, 255, 20, 0.4);
                padding: 20px;
                border-radius: 6px;
                text-align: center;
            }
            .metric-val-magenta {
                font-size: 2.2rem;
                color: #ff0055;
                text-shadow: 0 0 12px rgba(255, 0, 85, 0.8);
                font-weight: bold;
            }
            .metric-val-cyan {
                font-size: 2.2rem;
                color: #00f0ff;
                text-shadow: 0 0 12px rgba(0, 240, 255, 0.8);
                font-weight: bold;
            }
            .metric-val-green {
                font-size: 2.2rem;
                color: #39ff14;
                text-shadow: 0 0 12px rgba(57, 255, 20, 0.8);
                font-weight: bold;
            }
            .metric-lbl {
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 2px;
                color: #a0a0ab;
                margin-bottom: 5px;
            }
            hr {
                border: 0;
                height: 1px;
                background-image: linear-gradient(to right, rgba(0, 240, 255, 0), rgba(0, 240, 255, 0.75), rgba(0, 240, 255, 0));
                margin: 25px 0;
            }
        </style>
    """, unsafe_allow_html=True)

    initialize_application_state()
    
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    invoice_df = loop.run_until_complete(st.session_state.data_service.fetch_invoice_metrics())
    logs_df = loop.run_until_complete(st.session_state.data_service.fetch_communication_logs())

    with st.sidebar:
        st.markdown('<div class="sidebar-title">AEGIS DunEngine v1.0</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-metric"><span style="color:#a0a0ab">WORKER STATUS:</span> <span style="color:#39ff14; font-weight:bold; text-shadow: 0 0 5px #39ff14">ACTIVE</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-metric"><span style="color:#a0a0ab">DATABASE:</span> <span style="color:#39ff14; font-weight:bold; text-shadow: 0 0 5px #39ff14">CONNECTED</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-metric" style="border-color:#00f0ff"><span style="color:#a0a0ab">ENGINE CYCLE:</span> <span style="color:#00f0ff; font-weight:bold">5 MIN INTERVAL</span></div>', unsafe_allow_html=True)

    st.title("⚡ AUTOMATED DEBT RECOVERY OVERWATCH")
    st.markdown("---")

    overdue_mask = invoice_df["status"] == "OVERDUE"
    total_outstanding = invoice_df[overdue_mask]["amount"].sum() + invoice_df[overdue_mask]["accumulated_fees"].sum()
    active_delinquent_counts = invoice_df[overdue_mask]["customer_id"].nunique()
    mock_accuracy = 94.2

    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    with kpi_col1:
        st.markdown(f"""
            <div class="cyber-card-magenta">
                <div class="metric-lbl">Total Delinquent Debt</div>
                <div class="metric-val-magenta">${total_outstanding:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)
    with kpi_col2:
        st.markdown(f"""
            <div class="cyber-card-cyan">
                <div class="metric-lbl">Active Overdue Customers</div>
                <div class="metric-val-cyan">{active_delinquent_counts}</div>
            </div>
        """, unsafe_allow_html=True)
    with kpi_col3:
        st.markdown(f"""
            <div class="cyber-card-green">
                <div class="metric-lbl">Prediction Model Accuracy</div>
                <div class="metric-val-green">{mock_accuracy}%</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    st.subheader("📊 DEBT AGING VELOCITY MATRIX")
    aging_data = construct_aging_buckets(invoice_df)
    
    if not aging_data.empty:
        fig = go.Figure(data=[go.Bar(
            x=aging_data["Aging Bucket"],
            y=aging_data["Outstanding Balance"],
            marker=dict(
                color="rgba(255, 0, 85, 0.6)",
                line=dict(color="#ff0055", width=2)
            ),
            text=[f"${val:,.2f}" for val in aging_data["Outstanding Balance"]],
            textposition="auto",
            textfont=dict(family="Share Tech Mono", size=14, color="#ffffff")
        )])
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(10,10,12,1)",
            plot_bgcolor="rgba(13,13,17,1)",
            xaxis=dict(
                title="Aging Window", 
                gridcolor="rgba(0, 240, 255, 0.1)", 
                tickfont=dict(family="Orbitron", color="#00f0ff")
            ),
            yaxis=dict(
                title="Volume ($)", 
                gridcolor="rgba(0, 240, 255, 0.1)", 
                tickfont=dict(family="Share Tech Mono", color="#e0e0e6")
            ),
            margin=dict(l=40, r=40, t=20, b=40),
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No corporate elements identified in recovery lifecycle pipelines.")

    st.markdown("---")
    st.subheader("📡 DISPATCHED AUTOMATED DISPATCH AUDIT TRAIL")
    
    if not logs_df.empty:
        logs_df["risk_level"] = logs_df["action_taken"].apply(
            lambda x: "CRITICAL" if "Critical" in x else "LOW"
        )
        
        styled_rows = ""
        for _, row in logs_df.iterrows():
            ts = row["dispatched_at"].strftime("%Y-%m-%d %H:%M:%S")
            act = row["action_taken"]
            risk = row["risk_level"]
            
            risk_badge = f'<span style="color:#ff0055; border: 1px solid #ff0055; padding: 2px 6px; border-radius:3px; box-shadow: 0 0 5px #ff0055; font-size:0.8rem">CRITICAL</span>' if risk == "CRITICAL" else f'<span style="color:#39ff14; border: 1px solid #39ff14; padding: 2px 6px; border-radius:3px; box-shadow: 0 0 5px #39ff14; font-size:0.8rem">LOW</span>'
            action_color = "#ff0055" if risk == "CRITICAL" else "#00f0ff"
            
            
            styled_rows += f"""<tr style="border-bottom: 1px solid rgba(0, 240, 255, 0.15); background: rgba(13,13,17,0.5)">
<td style="padding:12px; font-family:'Share Tech Mono'; color:#a0a0ab">{ts}</td>
<td style="padding:12px; font-family:'Orbitron'; color:#00f0ff">{risk_badge}</td>
<td style="padding:12px; font-family:'Share Tech Mono'; color:{action_color}">{act}</td>
</tr>"""
            
        
        html_table = f"""<table style="width:100%; border-collapse: collapse; text-align: left;">
<thead>
<tr style="border-bottom: 2px solid #00f0ff; color: #00f0ff; font-family:'Orbitron'">
<th style="padding:12px;">TIMESTAMP</th>
<th style="padding:12px;">RISK PROFILE</th>
<th style="padding:12px;">AUTOMATED DISPATCH COMPONENT</th>
</tr>
</thead>
<tbody>
{styled_rows}
</tbody>
</table>"""
        st.markdown(html_table, unsafe_allow_html=True)
    else:
        st.info("No event sequences registered on active monitoring lanes.")

if __name__ == "__main__":
    render_dashboard()