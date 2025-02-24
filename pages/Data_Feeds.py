import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from functions.datafeeds_sql import *
import streamlit.components.v1 as components
from functions.session import download_pdf

st.title("📡 Data Feeds by Database Dashboard")
st.markdown("---")
download_pdf()

database_list = session.sql("SELECT DISTINCT DATABASE_NAME FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY").to_pandas()
database_options = database_list["DATABASE_NAME"].dropna().tolist()

database = st.selectbox("Select a Database", database_options, index=None, placeholder="Select a database...")

if database:
    queries_df = total_queries(database)
    credits_df = total_credits(database)
    users_df = unique_users(database)
    success_df = successful_queries(database)
    failed_df = failed_queries(database)
    queries_per_day_df = queries_per_day(database)
    unique_users_per_day_df = unique_users_per_day(database)
    total_queries_value = queries_df["TOTAL_QUERIES"].iloc[0] if not queries_df.empty else 0
    successful_queries_value = success_df.iloc[0, 0] if not success_df.empty else 0
    failed_queries_value = failed_df.iloc[0, 0] if not failed_df.empty else 0
    unique_users_value = users_df.iloc[0, 0] if not users_df.empty else 0
    total_credits_value = credits_df["TOTAL_QUERY_COST"].iloc[0] if not credits_df.empty else 0

    if total_queries_value > 0:
        success_percentage = (successful_queries_value / total_queries_value) * 100
        failed_percentage = (failed_queries_value / total_queries_value) * 100
    else:
        success_percentage = failed_percentage = 0

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(label="Successful Queries", value=f"{successful_queries_value}")
        st.markdown(f'<p style="font-weight:bold;">{success_percentage:.2f}% successful</p>', unsafe_allow_html=True)
    with col2:
        st.metric(label="Failed Queries", value=f"{failed_queries_value}")
        st.markdown(f'<p style="font-weight:bold;">{failed_percentage:.2f}% failed</p>', unsafe_allow_html=True)
    with col3:
        st.metric("Total Queries", total_queries_value)

    with col4:
        st.metric("Total Credits Used", total_credits_value)

    with col5:
        st.metric("Unique Users", unique_users_value)

    st.markdown("---")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Queries Per Day")
        if not queries_per_day_df.empty:
            queries_chart = alt.Chart(queries_per_day_df).mark_line(point=True).encode(
                x=alt.X("QUERY_DATE:T", title="Date"),
                y=alt.Y("QUERIES_COUNT:Q", title="Queries Count"),
                tooltip=["QUERY_DATE:T", "QUERIES_COUNT:Q"]
            ).properties(
                width="container",
                height=400
            )
            st.altair_chart(queries_chart, use_container_width=True)
        else:
            st.warning("No query data available.")

    with chart_col2:
        st.subheader("Unique Users Per Day")
        if not unique_users_per_day_df.empty:
            users_chart = alt.Chart(unique_users_per_day_df).mark_line(point=True).encode(
                x=alt.X("QUERY_DATE:T", title="Date"),
                y=alt.Y("UNIQUE_USERS:Q", title="Unique Users", scale=alt.Scale(domain=[1, max(unique_users_per_day_df['UNIQUE_USERS'].max(), 1)], zero=False)),
                tooltip=["QUERY_DATE:T", "UNIQUE_USERS:Q"]
            ).properties(
                width="container",
                height=400
            )
            st.altair_chart(users_chart, use_container_width=True)
        else:
            st.warning("No unique user data available.")

else:
    st.warning("Please select a database to display the data.")