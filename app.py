import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Visual Trend Dashboard",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #080c10; color: #d8dfe8; }
    [data-testid="stSidebar"] { background-color: #0d1219; border-right: 1px solid rgba(255,255,255,0.07); }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 8px;
        padding: 1rem;
    }
    [data-testid="stMetricLabel"] { color: #6a7888 !important; font-size: 0.75rem; letter-spacing: 0.1em; }
    [data-testid="stMetricValue"] { color: #e8c98a !important; font-size: 1.8rem; }
    [data-testid="stMetricDelta"] { color: #7eb8d4 !important; }

    /* Section headers */
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #c9a96e;
        border-bottom: 1px solid rgba(201,169,110,0.3);
        padding-bottom: 0.5rem;
        margin-bottom: 1.2rem;
        margin-top: 1.5rem;
    }

    /* Hero banner */
    .hero-banner {
        background: linear-gradient(135deg, #0d1219 0%, #111820 50%, #0d1219 100%);
        border: 1px solid rgba(201,169,110,0.2);
        border-radius: 12px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: radial-gradient(circle at 30% 50%, rgba(201,169,110,0.06) 0%, transparent 50%),
                    radial-gradient(circle at 70% 50%, rgba(126,184,212,0.06) 0%, transparent 50%);
    }
    .hero-title {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #e8c98a, #f0e0b8, #a8d4e8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .hero-sub {
        color: #6a7888;
        font-size: 0.85rem;
        letter-spacing: 0.1em;
        margin-top: 0.4rem;
    }

    /* Tag pills */
    .tag-pill {
        display: inline-block;
        background: rgba(201,169,110,0.1);
        border: 1px solid rgba(201,169,110,0.3);
        color: #e8c98a;
        border-radius: 20px;
        padding: 0.2rem 0.8rem;
        font-size: 0.7rem;
        letter-spacing: 0.1em;
        margin-right: 0.4rem;
    }

    /* Keyword bubble */
    .keyword-bubble {
        display: inline-block;
        background: rgba(126,184,212,0.08);
        border: 1px solid rgba(126,184,212,0.25);
        color: #a8d4e8;
        border-radius: 20px;
        padding: 0.3rem 1rem;
        font-size: 0.75rem;
        margin: 0.2rem;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #080c10; }
    ::-webkit-scrollbar-thumb { background: #c9a96e; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ─── Sample Data ───────────────────────────────────────────────────────────────
years = [2020, 2021, 2022, 2023, 2024]
styles = ["Cyberpunk", "Anime", "3D Render", "Retro Futurism", "Minimalism"]

trend_data = {
    "Year": years * len(styles),
    "Style": [s for s in styles for _ in years],
    "Popularity": [
        # Cyberpunk
        45, 62, 78, 85, 91,
        # Anime
        70, 75, 80, 88, 95,
        # 3D Render
        30, 48, 65, 74, 82,
        # Retro Futurism
        20, 35, 50, 63, 71,
        # Minimalism
        55, 60, 65, 68, 72,
    ]
}
df_trend = pd.DataFrame(trend_data)

tool_data = {
    "Tool": ["Midjourney", "DALL·E", "Stable Diffusion", "Adobe Firefly"],
    "Popularity": [92, 78, 85, 65],
    "Speed":      [70, 88, 82, 90],
    "Quality":    [95, 80, 78, 75],
    "Satisfaction": [90, 76, 80, 72],
    "Color": ["#e8c98a", "#7eb8d4", "#a06060", "#90c080"]
}
df_tools = pd.DataFrame(tool_data)

keyword_data = {
    "Keyword": ["cinematic lighting", "realistic portrait", "surreal art",
                "vaporwave", "hyperrealism", "neon glow", "dark fantasy",
                "studio lighting", "anime style", "oil painting"],
    "Frequency": [320, 285, 260, 210, 195, 180, 165, 150, 140, 125],
    "Growth": ["+45%", "+38%", "+52%", "+29%", "+61%", "+33%", "+28%", "+22%", "+35%", "+18%"]
}
df_keywords = pd.DataFrame(keyword_data)

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎛️ Dashboard Filters")
    st.markdown("---")

    selected_styles = st.multiselect(
        "🎨 Art Styles",
        options=styles,
        default=styles
    )

   
