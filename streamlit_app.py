import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SiS Performance Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊"
)

import pandas as pd
import plotly.express as px
from functions.queries_sql import *

# --- CUSTOM STYLING ---
custom_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: #0E1117;
            color: white;
        }
        h1, h2, h3, h4, h5 {
            color: #FFFFFF;
            font-weight: 600;
        }
        .big-title {
            font-size: 38px;
            font-weight: 700;
            text-align: center;
            color: #58A6FF;
        }
        .section-title {
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 10px;
            color: #E1E4E8;
            text-align: center;
        }
        .card {
            border-radius: 10px;
            background-color: #21262D;
            padding: 20px;
            text-align: center;
            box-shadow: 2px 2px 10px rgba(255, 255, 255, 0.1);
            transition: transform 0.2s;
        }
        .card:hover {
            transform: scale(1.05);
            background-color: #30363D;
        }
        .card-icon {
            font-size: 50px;
            color: #58A6FF;
            margin-bottom: 10px;
        }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown(
    """
    <div style="
        padding: 30px;
        border-radius: 12px;
        background: linear-gradient(135deg, #58A6FF, #1F6FEB);
        text-align: center;
        box-shadow: 2px 2px 10px rgba(255, 255, 255, 0.1);
    ">
        <h1 style="color: white; font-size: 42px; font-weight: 700; margin-bottom: 10px;">
            📊 SiS Performance Analytics
        </h1>
        <p style="color: white; font-size: 18px; font-weight: 400; max-width: 800px; margin: auto;">
            <b>A next-generation analytics platform</b> designed to monitor and optimize <b>SiS performance in Snowflake</b>.
            Gain insights into <b>queries, tasks, dynamic tables, credits, and data feeds</b> with real-time visualizations.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# --- FEATURE CARDS ---
st.markdown('<p class="section-title">🔍 Key Analytics Areas</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    with st.container():
        st.markdown(
            """
            <div class="card">
                <div class="card-icon">💰</div>
                <h3>Credits</h3>
                <p>Monitor credit consumption trends, usage over time, and remaining balances.</p>
            </div>
            """, unsafe_allow_html=True
        )

with col2:
    with st.container():
        st.markdown(
            """
            <div class="card">
                <div class="card-icon">📈</div>
                <h3>Queries</h3>
                <p>Analyze query performance by status, execution time, and failed queries.</p>
            </div>
            """, unsafe_allow_html=True
        )

with col3:
    with st.container():
        st.markdown(
            """
            <div class="card">
                <div class="card-icon">🛠️</div>
                <h3>Tasks & Tables</h3>
                <p>Track task refreshes, lag differences, and identify failed tasks & tables.</p>
            </div>
            """, unsafe_allow_html=True
        )

st.markdown("---")

col4, col5 = st.columns(2)

with col4:
    with st.container():
        st.markdown(
            """
            <div class="card">
                <div class="card-icon">📡</div>
                <h3>Data Feeds</h3>
                <p>Monitor query volume, credit consumption, and unique user trends.</p>
            </div>
            """, unsafe_allow_html=True
        )

with col5:
    with st.container():
        st.markdown(
            """
            <div class="card">
                <div class="card-icon">🚀</div>
                <h3>SiS Performance</h3>
                <p>Analyze SiS queries, success rates, and overall system efficiency.</p>
            </div>
            """, unsafe_allow_html=True
        )

st.markdown("---")

# --- LIVE METRICS OVERVIEW ---
st.markdown('<p class="section-title">📡 Live System Overview</p>', unsafe_allow_html=True)

df_summary = pd.DataFrame({
    "Metric": ["Total Queries", "Failed Queries (24h)", "Total Credits Used"],
    "Value": [
        queries_by_user()["TOTAL_QUERIES"].sum(),
        failed_queries_last_24_hours().shape[0],
        max_query_duration()  # Placeholder for total credits used
    ]
})

fig_summary = px.bar(
    df_summary,
    x="Value",
    y="Metric",
    orientation="h",
    text="Value",
    color="Metric",
    color_discrete_map={
        "Total Queries": "#58A6FF",
        "Failed Queries (24h)": "#E74C3C",
        "Total Credits Used": "#F39C12"
    },
    title="Live Performance Summary"
)
st.plotly_chart(fig_summary, use_container_width=True)
