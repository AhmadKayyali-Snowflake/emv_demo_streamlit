import streamlit as st
import pandas as pd
import plotly.express as px
from functions.queries_sql import *
from functions.credits_sql import *

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SiS Performance Analytics",
    layout="wide",
    page_icon="📊"
)

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
            margin-bottom: 10px;
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
        Snowflake Performance Analytics
        </h1>
        <p style="color: white; font-size: 18px; font-weight: 400; max-width: 800px; margin: auto;">
            Analytics platform designed to monitor and optimize performance in Snowflake.
            Gain insights into queries, tasks, dynamic tables, credits, and data feeds with real-time visualizations.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# --- NAVIGATION BUTTONS BELOW HTML CARDS ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="card">
            <div class="card-icon">💰</div>
            <h3>Credit Usage</h3>
            <p>Monitor credit consumption trends, usage over time, and remaining balances.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Go to Credit Usage", key="credit_usage", use_container_width=True):
        st.switch_page("pages/Credit_Usage.py")

with col2:
    st.markdown(
        """
        <div class="card">
            <div class="card-icon">📈</div>
            <h3>Query Monitoring</h3>
            <p>Analyze query performance by status, execution time, and failed queries.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Go to Query Monitoring", key="query_monitoring", use_container_width=True):
        st.switch_page("pages/Query_Monitoring.py")

with col3:
    st.markdown(
        """
        <div class="card">
            <div class="card-icon">🛠️</div>
            <h3>Tasks & Tables Monitoring</h3>
            <p>Track task refreshes, lag differences, and identify failed tasks & tables.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # if st.button("Go to Tasks & Tables", key="tasks", use_container_width=True):
    #     st.switch_page("pages/tasks.py")

st.markdown("---")

col4, col5 = st.columns(2)

with col4:
    st.markdown(
        """
        <div class="card">
            <div class="card-icon">📡</div>
            <h3>Data Feeds</h3>
            <p>Monitor query volume, credit consumption, and unique user trends.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Go to Data Feeds", key="data_feeds", use_container_width=True):
        st.switch_page("pages/Data_Feeds.py")

with col5:
    st.markdown(
        """
        <div class="card">
            <div class="card-icon">🚀</div>
            <h3>SiS Performance</h3>
            <p>Analyze SiS queries, success rates, and overall system efficiency.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # if st.button("Go to SiS Performance", key="sis_performance"):
    #     st.switch_page("pages/sis_performancer.py")

# st.markdown("---")

# # --- LIVE METRICS OVERVIEW ---
# st.subheader("📊 Live Performance Summary")

# # Fetch data from SQL functions
# total_queries = queries_by_user()["TOTAL_QUERIES"].sum()
# failed_queries = failed_queries_last_24_hours().shape[0]
# credits_used_total = credits_used()

# df_summary = pd.DataFrame({
#     "Metric": ["Total Queries", "Failed Queries (24h)", "Total Credits Used"],
#     "Value": [total_queries, failed_queries, credits_used_total]
# })

# fig_summary = px.bar(
#     df_summary,
#     x="Value",
#     y="Metric",
#     orientation="h",
#     text="Value",
#     color="Metric",
#     title="Live Performance Summary"
# )
# st.plotly_chart(fig_summary, use_container_width=True)
