import streamlit as st
import pandas as pd
import plotly.express as px
from functions.tasks_sql import *

st.set_page_config(
    layout="wide",
    page_icon="🛠️"
)

# --- FETCH DATA ---
df_tasks_status = tasks_by_refresh_status()
max_task_lag = max_task_lag_difference()
df_failed_tasks = failed_tasks_last_24_hours()

# --- HEADER ---
st.title("🛠️ Task Execution Dashboard")
st.markdown("An interactive **real-time** overview of task execution, failures, and performance metrics.")

st.markdown("---")

# --- PERFORMANCE OVERVIEW SECTION ---
st.markdown("### ⏳ Task Execution Performance")

col1, col2 = st.columns((2, 3))

# --- METRIC CARD FOR MAX TASK EXECUTION LAG ---
with col1:
    st.markdown("""
    <div style="
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #58A6FF, #1F6FEB);
        text-align: center;
        box-shadow: 2px 2px 10px rgba(255, 255, 255, 0.1);
    ">
        <h2 style="color: white; font-size: 22px; font-weight: 600; margin-bottom: 5px;">
            Max Task Execution Lag
        </h2>
        <p style="color: white; font-size: 26px; font-weight: 700;">
            {lag:.2f} seconds
        </p>
    </div>
    """.format(lag=max_task_lag), unsafe_allow_html=True)

# --- TASK EXECUTION LAG DISTRIBUTION ---
with col2:
    st.subheader("⏳ Task Execution Lag Distribution")

    # Define categories
    lag_distribution = pd.DataFrame({
        "Category": ["Fast (Under 30s)", "Moderate (30s - 5min)", "Slow (Over 5min)"],
        "Seconds": [30, 270, max(max_task_lag - 300, 0)]  # Ensure a valid scale
    })

    # Assign colors
    category_colors = {
        "Fast (Under 30s)": "#2ECC71",  # Green
        "Moderate (30s - 5min)": "#F39C12",  # Yellow
        "Slow (Over 5min)": "#E74C3C"  # Red
    }

    # Create a horizontal bar chart
    fig_lag = px.bar(
        lag_distribution,
        x="Seconds",
        y="Category",
        orientation="h",
        text="Seconds",
        color="Category",
        color_discrete_map=category_colors,
        title="Task Execution Time Breakdown"
    )

    fig_lag.update_layout(
        xaxis_title="Execution Time (Seconds)",
        yaxis_title="Category",
        showlegend=False
    )

    st.plotly_chart(fig_lag, use_container_width=True)

st.markdown("---")

# --- TABS FOR NAVIGATION ---
tab1, tab2 = st.tabs(["📊 Task Execution Status", "❌ Failed Tasks"])

# --- TAB 1: TASK EXECUTION STATUS ---
with tab1:
    col1, col2 = st.columns((5, 5))

    with col1:
        st.subheader("✅ Task Volume by Execution Status")

        # Assign colors manually for better distinction
        status_colors = {
            "SUCCEEDED": "#2ECC71",  # Green
            "FAILED": "#E74C3C",  # Red
            "SCHEDULED": "#F39C12",  # Yellow/Orange
            "EXECUTE_TASK": "#1ABC9C",  # Teal
            "UNKNOWN": "#BDC3C7"  # Grey for other states
        }

        # Map colors for consistency
        df_tasks_status["COLOR"] = df_tasks_status["STATE"].map(status_colors)

        fig_status = px.pie(
            df_tasks_status,
            names="STATE",
            values="COUNT",
            hole=0.4,  # Donut Chart Effect
            title="Task Execution Status",
            color="STATE",
            color_discrete_map=status_colors
        )
        st.plotly_chart(fig_status, use_container_width=True)

# --- TAB 2: FAILED TASKS ---
with tab2:
    st.subheader("❌ Failed Tasks in the Last 24 Hours")

    if df_failed_tasks.empty:
        st.info("No failed tasks in the last 24 hours.")
    else:
        st.data_editor(
            df_failed_tasks,
            use_container_width=True,
            height=250,
            hide_index=True
        )
