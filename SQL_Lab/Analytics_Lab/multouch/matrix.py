import asyncio
import sys
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import plotly.express as px  
import plotly.io as pio
from pydantic import BaseModel, Field
import streamlit as st
from loguru import logger
from sqlalchemy import Float, Integer, String, Text
from sqlalchemy.pool import NullPool 
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column  

logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
)

DATABASE_URL = "sqlite+aiosqlite:///neon_matrix.db"

class Base(DeclarativeBase):
    pass

class JourneyRecord(Base):
    __tablename__ = "customer_journeys"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(50), nullable=False)
    touchpoints: Mapped[str] = mapped_column(Text, nullable=False)
    timestamps: Mapped[str] = mapped_column(Text, nullable=False)
    revenue: Mapped[float] = mapped_column(Float, default=0.0)
    converted: Mapped[int] = mapped_column(Integer, default=0)

class ChannelCostRecord(Base):
    __tablename__ = "channel_costs"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    channel: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    cost: Mapped[float] = mapped_column(Float, nullable=False)

class DatabaseManager:
    def __init__(self, url: str):
        self.engine = create_async_engine(url, echo=False, poolclass=NullPool)
        self.session_factory = async_sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    async def initialize_schemas(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database schemas initialized.")

    async def seed_data_if_empty(self):
        async with self.session_factory() as session:
            from sqlalchemy import select, func
            result = await session.execute(select(func.count(JourneyRecord.id)))
            count = result.scalar()
            if count and count > 0:
                return

            logger.info("Database is empty. Initiating mock generation engine...")
            
            costs = {
                "Google Ads": 12000.0,
                "Facebook Ads": 9500.0,
                "Instagram": 7000.0,
                "TikTok": 8500.0,
                "Email": 1500.0,
                "Direct": 0.0,
                "Referral": 1200.0
            }
            for ch, cost in costs.items():
                session.add(ChannelCostRecord(channel=ch, cost=cost))

            np.random.seed(42)
            base_time = datetime.now() - timedelta(days=30)
            channels_pool = list(costs.keys())
            
            for i in range(1, 1201):
                user_id = f"USR-{i:05d}"
                rand_val = np.random.rand()
                if rand_val < 0.25:
                    tps = ["Google Ads", "Instagram", "Email"]
                    revenue = float(np.random.normal(600, 150))
                    converted = 1
                elif rand_val < 0.45:
                    tps = ["TikTok", "Instagram"]
                    revenue = float(np.random.normal(200, 50))
                    converted = 1
                elif rand_val < 0.65:
                    tps = ["Facebook Ads", "Google Ads", "Direct", "Email"]
                    revenue = float(np.random.normal(1100, 250))
                    converted = 1
                elif rand_val < 0.85:
                    tps = [np.random.choice(["Direct", "Referral"]), "Email"]
                    revenue = float(np.random.normal(120, 30))
                    converted = 1
                else:
                    path_len = np.random.randint(1, 4)
                    tps = list(np.random.choice(channels_pool, size=path_len))
                    revenue = 0.0
                    converted = 0
                
                revenue = max(0.0, round(revenue, 2)) if converted == 1 else 0.0
                
                times = []
                current_tp_time = base_time + timedelta(days=np.random.uniform(0, 28))
                for _ in tps:
                    times.append(str(int(current_tp_time.timestamp())))
                    current_tp_time += timedelta(hours=np.random.uniform(2, 48))

                session.add(JourneyRecord(
                    user_id=user_id,
                    touchpoints=";".join(tps),
                    timestamps=";".join(times),
                    revenue=revenue,
                    converted=converted
                ))
            
            await session.commit()
            logger.info("Database successfully loaded with comprehensive mock validation sequences.")

    async def fetch_analytics_dataset(self):
        async with self.session_factory() as session:
            from sqlalchemy import select
            journey_stmt = select(JourneyRecord)
            cost_stmt = select(ChannelCostRecord)
            
            j_res = await session.execute(journey_stmt)
            c_res = await session.execute(cost_stmt)
            
            journeys = j_res.scalars().all()
            costs = c_res.scalars().all()
            
            return journeys, costs

db_manager = DatabaseManager(DATABASE_URL)

class ValidatedJourney(BaseModel):
    user_id: str = Field(..., min_length=3)
    touchpoints: list[str] = Field(..., min_length=1)
    timestamps: list[int] = Field(..., min_length=1)
    revenue: float = Field(..., ge=0.0)
    converted: int = Field(..., ge=0, le=1)

class ValidatedCost(BaseModel):
    channel: str
    cost: float = Field(..., ge=0.0)

def validate_and_transform_data(raw_journeys, raw_costs) -> tuple[list[ValidatedJourney], dict[str, float]]:
    clean_journeys = []
    for r in raw_journeys:
        try:
            v = ValidatedJourney(
                user_id=r.user_id,
                touchpoints=r.touchpoints.split(";"),
                timestamps=[int(x) for x in r.timestamps.split(";")],
                revenue=r.revenue,
                converted=r.converted
            )
            clean_journeys.append(v)
        except Exception as e:
            logger.error(f"Pydantic parsing isolation alert on record {r.id}: {e}")
            continue

    cost_map = {}
    for c in raw_costs:
        try:
            v = ValidatedCost(channel=c.channel, cost=c.cost)
            cost_map[v.channel] = v.cost
        except Exception as e:
            logger.error(f"Pydantic parsing isolation alert on cost mapping table structural segment: {e}")
            continue
            
    return clean_journeys, cost_map

class AttributionEngine:
    def __init__(self, journeys: list[ValidatedJourney], costs: dict[str, float]):
        self.journeys = journeys
        self.costs = costs
        self.channels = list(costs.keys())

    def compute_first_click(self) -> dict[str, float]:
        allocation = {c: 0.0 for c in self.channels}
        for j in self.journeys:
            if j.converted == 1 and j.touchpoints:
                first_ch = j.touchpoints[0]
                if first_ch in allocation:
                    allocation[first_ch] += j.revenue
        return allocation

    def compute_last_click(self) -> dict[str, float]:
        allocation = {c: 0.0 for c in self.channels}
        for j in self.journeys:
            if j.converted == 1 and j.touchpoints:
                last_ch = j.touchpoints[-1]
                if last_ch in allocation:
                    allocation[last_ch] += j.revenue
        return allocation

    def compute_linear(self) -> dict[str, float]:
        allocation = {c: 0.0 for c in self.channels}
        for j in self.journeys:
            if j.converted == 1 and j.touchpoints:
                n = len(j.touchpoints)
                split_rev = j.revenue / n
                for ch in j.touchpoints:
                    if ch in allocation:
                        allocation[ch] += split_rev
        return allocation

    def compute_time_decay(self, half_life_days: float = 7.0) -> dict[str, float]:
        allocation = {c: 0.0 for c in self.channels}
        for j in self.journeys:
            if j.converted == 1 and j.touchpoints:
                t_max = j.timestamps[-1]
                weights = []
                for t in j.timestamps:
                    days_diff = (t_max - t) / 86400.0
                    w = 2 ** (-days_diff / half_life_days)
                    weights.append(w)
                
                total_w = sum(weights)
                if total_w == 0:
                    total_w = 1.0
                
                for ch, w in zip(j.touchpoints, weights):
                    if ch in allocation:
                        allocation[ch] += (w / total_w) * j.revenue
        return allocation

    def compute_data_driven_markov(self) -> dict[str, float]:
        allocation = {c: 0.0 for c in self.channels}
        transition_counts = {}
        
        for j in self.journeys:
            path = ["(Start)"]
            for ch in j.touchpoints:
                if not path or path[-1] != ch:
                    path.append(ch)
            
            if j.converted == 1:
                path.append("(Conversion)")
            else:
                path.append("(Dropoff)")
                
            for i in range(len(path) - 1):
                state_from = path[i]
                state_to = path[i+1]
                if state_from not in transition_counts:
                    transition_counts[state_from] = {}
                transition_counts[state_from][state_to] = transition_counts[state_from].get(state_to, 0) + 1

        transition_matrix = {}
        for state_from, targets in transition_counts.items():
            total_outventions = sum(targets.values())
            transition_matrix[state_from] = {st: count / total_outventions for st, count in targets.items()}

        def calculate_conversion_probability(matrix_instance) -> float:
            state_probs = {"(Start)": 1.0}
            for _ in range(15):
                next_probs = {}
                for s, p in state_probs.items():
                    if s in ["(Conversion)", "(Dropoff)"]:
                        next_probs[s] = next_probs.get(s, 0.0) + p
                        continue
                    if s in matrix_instance:
                        for target, trans_p in matrix_instance[s].items():
                            next_probs[target] = next_probs.get(target, 0.0) + (p * trans_p)
                state_probs = next_probs
            return state_probs.get("(Conversion)", 0.0)

        base_prob = calculate_conversion_probability(transition_matrix)
        if base_prob == 0:
            base_prob = 1.0

        removal_effects = {}
        for ch in self.channels:
            if ch not in transition_matrix:
                removal_effects[ch] = 0.0
                continue
                
            altered_matrix = {}
            for s_from, targets in transition_matrix.items():
                if s_from == ch:
                    continue
                altered_matrix[s_from] = {}
                for s_to, p in targets.items():
                    if s_to == ch:
                        altered_matrix[s_from]["(Dropoff)"] = altered_matrix[s_from].get("(Dropoff)", 0.0) + p
                    else:
                        altered_matrix[s_from][s_to] = p
                        
            altered_prob = calculate_conversion_probability(altered_matrix)
            removal_effects[ch] = (base_prob - altered_prob) / base_prob

        total_effects = sum(removal_effects.values())
        if total_effects == 0:
            total_effects = 1.0

        total_converted_revenue = sum(j.revenue for j in self.journeys if j.converted == 1)
        for ch in self.channels:
            allocation[ch] = (removal_effects.get(ch, 0.0) / total_effects) * total_converted_revenue
            
        return allocation

st.set_page_config(
    page_title="NEON MATRIX // Attribution Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def startup_pipeline_executor():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(db_manager.initialize_schemas())
        loop.run_until_complete(db_manager.seed_data_if_empty())
    finally:
        loop.close()  
    logger.info("Startup orchestration phase verified complete.")
    return True

startup_pipeline_executor()

@st.cache_data(ttl=600)
def load_and_cache_dataset():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        raw_j, raw_c = loop.run_until_complete(db_manager.fetch_analytics_dataset())
    finally:
        loop.close()
    clean_j, clean_c = validate_and_transform_data(raw_j, raw_c)
    return clean_j, clean_c

validated_journeys, validated_costs = load_and_cache_dataset()
engine = AttributionEngine(validated_journeys, validated_costs)

st.markdown("""
    <style>
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #0a0a12 !important;
            color: #e2e8f0 !important;
            font-family: 'Courier New', Courier, monospace;
        }
        
        [data-testid="stSidebar"] {
            background-color: #0d0e15 !important;
            border-right: 2px solid #00f0ff !important;
            box-shadow: 0 0 15px rgba(0, 240, 255, 0.2);
        }
        
        h1, h2, h3 {
            color: #00f0ff !important;
            text-shadow: 0 0 10px rgba(0, 240, 255, 0.6), 0 0 20px rgba(0, 240, 255, 0.3);
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        div.stButton > button {
            background-color: #1a1a2e !important;
            color: #00f0ff !important;
            border: 2px solid #00f0ff !important;
            border-radius: 4px;
            box-shadow: 0 0 8px rgba(0, 240, 255, 0.4);
            transition: all 0.3s ease-in-out;
            font-weight: bold;
        }
        div.stButton > button:hover {
            color: #ffffff !important;
            background-color: #00f0ff !important;
            box-shadow: 0 0 20px #00f0ff, 0 0 40px #ff0055;
            border-color: #ff0055 !important;
        }
        
        .kpi-container {
            background-color: #1a1a2e !important;
            border: 2px solid #ff0055 !important;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 0 15px rgba(255, 0, 85, 0.3);
            margin-bottom: 25px;
        }
        .kpi-title {
            font-size: 0.85rem;
            color: #00f0ff !important;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 10px;
        }
        .kpi-value {
            font-size: 2rem;
            font-weight: bold;
            color: #ffffff !important;
            text-shadow: 0 0 12px rgba(255, 255, 255, 0.8);
        }
        
        .stSelectbox label {
            color: #00f0ff !important;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ NEON MATRIX // MULTI-TOUCH ATTRIBUTION ENGINE")
st.markdown("---")

st.sidebar.markdown("### 🛠️ CONTROL INTERFACE")
selected_model = st.sidebar.selectbox(
    "SELECT MATHEMATICAL ATTRIBUTION LAYER:",
    ["First Click", "Last Click", "Linear", "Time Decay (7d Half-Life)", "Data-Driven (Markov Chain)"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
    **SYSTEM STATUS:** <span style='color:#00f0ff; font-weight:bold;'>ONLINE</span><br>
    **DATABASE CORE:** <span style='color:#ff0055; font-weight:bold;'>SQLITE.ASYNC</span><br>
    **VALIDATION RIG:** <span style='color:#00f0ff; font-weight:bold;'>PYDANTIC V2</span>
""", unsafe_allow_html=True)

if selected_model == "First Click":
    channel_revenues = engine.compute_first_click()
elif selected_model == "Last Click":
    channel_revenues = engine.compute_last_click()
elif selected_model == "Linear":
    channel_revenues = engine.compute_linear()
elif selected_model == "Time Decay (7d Half-Life)":
    channel_revenues = engine.compute_time_decay()
else:
    channel_revenues = engine.compute_data_driven_markov()

total_revenue = sum(channel_revenues.values())
total_spend = sum(validated_costs.values())
overall_roi = ((total_revenue - total_spend) / total_spend) * 100 if total_spend > 0 else 0.0

top_channel = "N/A"
max_rev = -1.0
for ch, rev in channel_revenues.items():
    if rev > max_rev:
        max_rev = rev
        top_channel = ch

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-title">TOTAL REVENUE ALLOCATION</div>
            <div class="kpi-value">${total_revenue:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-title">TOTAL SYSTEM MARKETING SPEND</div>
            <div class="kpi-value">${total_spend:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-title">AGGREGATE MARKETING ROI</div>
            <div class="kpi-value">{overall_roi:.1f}%</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-title">ALPHA DOMINANT CHANNEL</div>
            <div class="kpi-value" style="color:#00f0ff;">{top_channel}</div>
        </div>
    """, unsafe_allow_html=True)

channels_list = list(validated_costs.keys())
chart_data = []
for ch in channels_list:
    rev = channel_revenues.get(ch, 0.0)
    cost = validated_costs.get(ch, 0.0)
    roi = ((rev - cost) / cost) * 100 if cost > 0 else 0.0
    chart_data.append({"Channel": ch, "Revenue": round(rev, 2), "Ad Spend": round(cost, 2), "ROI (%)": round(roi, 2)})

df_metrics = pd.DataFrame(chart_data)

cyber_colors = ["#00f0ff", "#ff0055", "#9d4edd", "#ff9e00", "#2ec4b6", "#e0aaff", "#70e000"]

st.markdown("### 📊 MULTI-TOUCH ANALYTICAL FORECASTS")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    fig_bar = px.bar(
        df_metrics, 
        x="Channel", 
        y=["Revenue", "Ad Spend"],
        barmode="group",
        title=f"REVENUE VS SPEND ANALYSIS ({selected_model.upper()})",
        color_discrete_sequence=["#00f0ff", "#ff0055"],
        template="plotly_dark"
    )
    fig_bar.update_layout(
        plot_bgcolor="#0d0e15",
        paper_bgcolor="#0a0a12",
        font_family="Courier New",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#1a1a2e")
    )
    st.plotly_chart(fig_bar, width='stretch', key="neon_bar_chart")

with chart_col2:
    fig_pie = px.pie(
        df_metrics, 
        names="Channel", 
        values="Revenue",
        hole=0.4,
        title="REVENUE DISPERSION RADIAL WEIGHT",
        color_discrete_sequence=cyber_colors,
        template="plotly_dark"
    )
    fig_pie.update_layout(
        plot_bgcolor="#0d0e15",
        paper_bgcolor="#0a0a12",
        font_family="Courier New"
    )
    st.plotly_chart(fig_pie, width='stretch', key="neon_pie_chart")

st.markdown("### 🎛️ CROSS-CHANNEL GRANULAR PERFORMANCE LEDGER")
st.dataframe(
    df_metrics.style.background_gradient(cmap="Purples", subset=["Revenue", "ROI (%)"]),
    width='stretch'
)