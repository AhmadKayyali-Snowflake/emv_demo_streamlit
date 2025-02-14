import streamlit as st
st.set_page_config(
    page_title="SiS Performance Analytics",
    layout="wide",
    page_icon="📊"
)
import pandas as pd
import plotly.express as px
from functions.queries_sql import *
from functions.credits_sql import *

custom_css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
            background-color: "#0E1117"
            color: white;
        }}
        h1{{
            color: white;
            font-weight: 600;
        }}
        h2, h3, h4, h5 {{
            color: white;
            font-weight: 600;
        }}
        .big-title {{
            font-size: 38px;
            font-weight: 700;
            text-align: center;
            color: white;
        }}
        .section-title {{
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 10px;
            color: white;
            text-align: center;
        }}
        .card {{
            border-radius: 10px;
            background-color: #5D5C61;
            padding: 20px;
            text-align: center;
            box-shadow: 2px 2px 10px rgba(255, 255, 255, 0.1);
            transition: transform 0.2s, background-color 0.3s;
            margin-bottom: 10px;
        }}
        .card:hover h3 {{
            color: white;
        }}
        .card:hover {{
            transform: scale(1.05);
            background-color: #1F6FEB;
            color: white;
        }}
        .card-icon {{
            font-size: 50px;
            color: white;
            margin-bottom: 10px;
        }}
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.markdown(
    f"""
    <div style="
        padding: 30px;
        border-radius: 12px;
        background: linear-gradient(135deg, #1F6FEB, #1F6FEB);
        text-align: center;
        box-shadow: 2px 2px 10px rgba(255, 255, 255, 0.1);
    ">
        <h1 style="color:white; font-size: 42px; font-weight: 700; margin-bottom: 10px;">
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

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="card">
            <div class="card-icon">💰</div>
            <h3 style="color: white;">Credit Usage</h3>
            <p style="color:whrite;">Monitor credit consumption trends, usage over time, and remaining balances.</p>
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
            <h3 style="color: white;">Query Monitoring</h3>
            <p style="color:white;">Analyze query performance by status, execution time, and failed queries.</p>
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
            <h3 style="color: white;">Tasks & Tables</h3>
            <p style="color:white;">Track task refreshes, lag differences, and identify failed tasks & tables.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Go to Tasks & Dynamic Tables", key="tasks", use_container_width=True):
        st.switch_page("pages/Tasks_&_Dynamic_Tables.py")

st.markdown("---")

col4, col5 = st.columns(2)

with col4:
    st.markdown(
        """
        <div class="card">
            <div class="card-icon">📡</div>
            <h3 style="color: white;">Data Feeds</h3>
            <p style="color:white;">Monitor query volume, credit consumption, and unique user trends.</p>
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
            <h3 style="color: white;">SiS Performance</h3>
            <p style="color:white;">Analyze SiS queries, success rates, and overall system efficiency.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )