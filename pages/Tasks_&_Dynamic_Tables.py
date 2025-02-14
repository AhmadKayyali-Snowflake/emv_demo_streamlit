import streamlit as st
import pandas as pd
import plotly.express as px
from functions.tasks_sql import *

df_tasks_status = tasks_by_refresh_status()
max_task_lag = max_task_lag_difference()
df_failed_tasks = failed_tasks_last_24_hours()

df_dynamic_tables_status = dynamic_tables_by_refresh_status()
max_dynamic_tables_lag = max_dynamic_tables_lag_difference()
df_failed_dynamic_tables = failed_dynamic_tables_last_24_hours()

df_failed_tasks = df_failed_tasks if df_failed_tasks is not None else pd.DataFrame(columns=["STATE"])
df_failed_dynamic_tables = df_failed_dynamic_tables if df_failed_dynamic_tables is not None else pd.DataFrame(columns=["STATE"])

st.title("🛠️ Task & Dynamic Table Execution Dashboard")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.metric(label="Max Task Lag", value=f"{max_task_lag} seconds", delta_color="inverse")
with col2:
    st.metric(label="Failed Tasks in Last 24hrs", value=f"{len(df_failed_tasks)}", delta_color="inverse")
status_colors = {
    "SUCCEEDED": "#2ECC71",  
    "FAILED": "#E74C3C",  
    "CANCELLED": "#F39C12",
    "SKIPPED": "#A0A0A0"
}

df_tasks_status["COLOR"] = df_tasks_status["REFRESH_STATUS"].map(status_colors)

st.subheader("Tasks Status")

fig_status = px.bar(
    df_tasks_status,
    x="REFRESH_STATUS",
    y="TASK_COUNT",
    color="REFRESH_STATUS",
    color_discrete_map=status_colors,
    text_auto=True,
    height=400
)

fig_status.update_layout(xaxis_title="Task Status", yaxis_title="Task Count")

st.plotly_chart(fig_status, use_container_width=True)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.metric(label="Max Dynamic Tables Lag", value=f"{max_dynamic_tables_lag} seconds", delta_color="inverse")
with col2:
    st.metric(label="Failed Dynamic Tables in Last 24hrs", value=f"{len(df_failed_dynamic_tables)}", delta_color="inverse")
status_colors = {
    "SCHEDULED": "#3498DB",
    "EXECUTING": "#F1C40F",
    "SUCCEEDED": "#2ECC71",
    "FAILED": "#E74C3C",
    "CANCELLED": "#F39C12",
    "UPSTREAM_FAILED": "#8E44AD"
}

df_dynamic_tables_status["COLOR"] = df_dynamic_tables_status["REFRESH_STATUS"].map(status_colors)

st.subheader("Dynamic Tables Status")

fig_status = px.bar(
    df_dynamic_tables_status,
    x="REFRESH_STATUS",
    y="DYNAMIC_TABLE_COUNT",
    color="REFRESH_STATUS",
    color_discrete_map=status_colors,
    text_auto=True,
    height=400
)

fig_status.update_layout(xaxis_title="Dynamic Table Status", yaxis_title="Dynamic Table Count")

st.plotly_chart(fig_status, use_container_width=True)
