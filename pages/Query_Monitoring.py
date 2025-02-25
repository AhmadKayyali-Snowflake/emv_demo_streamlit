import streamlit as st
import pandas as pd
import plotly.express as px
from functions.queries_sql import *
import streamlit.components.v1 as components
from functions.session import download_pdf

df_queries_by_user = queries_by_user()
df_query_status = query_volume_by_status()
df_failed_queries = failed_queries_last_24_hours()
max_duration = max_query_duration()
df_longest_queries = longest_queries_last_24_hours()

st.title("📈 Query Monitoring Dashboard")
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Max Query Duration (min)", value=f"{max_duration:.2f}", delta_color="inverse")

with col2:
    st.metric(label="Number of Failed Queries last 24hrs", value=f"{number_failed_queries_last_24_hours()}", delta_color="inverse")
with col3:
    st.metric(label="Total Number of Queries", value=f"{df_queries_by_user['TOTAL_QUERIES'].sum()}", delta_color="inverse")

download_pdf()
st.markdown("---")

st.write("")
main_cols = st.columns(2)

with main_cols[0]:

    status_colors = {
        "SUCCESS": "#2ECC71",
        "FAIL": "#E74C3C",
        "INCIDENT": "#F39C12"
    }

    df_query_status["COLOR"] = df_query_status["EXECUTION_STATUS"].map(status_colors)

    st.subheader("Query Volume by Execution Status")

    fig_status = px.pie(
        df_query_status,
        names="EXECUTION_STATUS",
        values="QUERY_COUNT",
        color="EXECUTION_STATUS",
        hole=0.6,
        color_discrete_map=status_colors,
        height=400
    )
    st.plotly_chart(fig_status, use_container_width=True)

with main_cols[1]:
    st.subheader("Failed Queries in the Last 24 Hours")
    st.data_editor(
        df_failed_queries,
        use_container_width=True,
        height=400,
        hide_index=True
    )
st.markdown("---")
st.subheader("Queries Executed by User")
user_list = df_queries_by_user["USER_NAME"].unique()
selected_user = st.selectbox("Filter by User:", ["All"] + list(user_list))

if selected_user != "All":
    df_filtered_users = df_queries_by_user[df_queries_by_user["USER_NAME"] == selected_user]
else:
    df_filtered_users = df_queries_by_user

fig_users = px.bar(
    df_filtered_users,
    x="TOTAL_QUERIES",
    y="USER_NAME",
    orientation="h",
    color="TOTAL_QUERIES",
    color_continuous_scale="blues"
)
st.plotly_chart(fig_users, use_container_width=True)

st.markdown("---")

st.subheader("Longest Queries in the Last 24 Hours")
st.data_editor(
    df_longest_queries,
    use_container_width=True,
    height=300,
    hide_index=True
)