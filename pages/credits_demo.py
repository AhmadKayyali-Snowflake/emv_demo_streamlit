import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
# Title
st.title(":credit_card: Credits Usage Dashboard")
st.write("Monitor total credits used, percentage used, remaining credits, and credit trends.")
# :pushpin: **Simulated Data (Replace with Snowflake Queries)**
credits_data = pd.DataFrame({
    "warehouse": ["WH_A", "WH_B", "WH_C", "WH_D"],
    "credits_used": [1200, 900, 700, 400],
    "latitude": [37.7749, 34.0522, 40.7128, 51.5074],  # Example Latitudes (San Francisco, LA, NY, London)
    "longitude": [-122.4194, -118.2437, -74.0060, -0.1278]  # Example Longitudes
})
time_series_data = pd.DataFrame({
    "month": pd.date_range(start="2024-01-01", periods=12, freq="M"),
    "credits_used": [300, 350, 400, 450, 500, 600, 700, 750, 800, 850, 900, 950]
})
# :pushpin: **Metrics**
total_credits = 10000  # Example total credit limit
total_credits_used = credits_data["credits_used"].sum()
percentage_used = (total_credits_used / total_credits) * 100
remaining_credits = total_credits - total_credits_used
# :art: **ROW 1: Metrics**
col1, col2, col3 = st.columns(3)
col1.metric(label=":credit_card: Total Credits Used", value=f"{total_credits_used:,}")
col2.metric(label=":bar_chart: % of Credits Used", value=f"{percentage_used:.2f}%")
col3.metric(label=":chart_with_downwards_trend: Total Credits Remaining", value=f"{remaining_credits:,}")
# Divider
st.markdown("---")
# :art: **ROW 2: Donut Chart & Line Chart (Side-by-Side)**
col4, col5 = st.columns([1, 2])
with col4:
    st.subheader(":radio_button: Credit Usage Breakdown")
    fig_pie = px.pie(
        credits_data,
        names="warehouse",
        values="credits_used",
        hole=0.4,  # Donut Chart (Pie Chart with a hole)
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    st.plotly_chart(fig_pie, use_container_width=True)
with col5:
    st.subheader(":date: Credits Used Over Time (Monthly)")
    fig_line = px.line(
        time_series_data,
        x="month",
        y="credits_used",
        markers=True,
        title="Monthly Credit Consumption",
        line_shape="spline",
        color_discrete_sequence=["#2E86C1"]
    )
    st.plotly_chart(fig_line, use_container_width=True)
# :art: **ROW 3: Bar Chart & Choropleth Map (Side-by-Side)**
col6, col7 = st.columns([1, 2])
with col6:
    st.subheader(":office: Credits Used by Warehouse")
    chart = alt.Chart(credits_data).mark_bar(color="steelblue").encode(
        x="warehouse",
        y="credits_used",
        tooltip=["warehouse", "credits_used"]
    ).properties(width=400)
    st.altair_chart(chart, use_container_width=True)
with col7:
    st.subheader(":earth_africa: Warehouse Credit Usage by Location")
    fig_map = px.scatter_mapbox(
        credits_data,
        lat="latitude",
        lon="longitude",
        size="credits_used",
        hover_name="warehouse",
        title="Warehouse Credit Usage (Geographical View)",
        color="credits_used",
        color_continuous_scale=px.colors.sequential.Plasma,
        zoom=1
    )
    fig_map.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig_map, use_container_width=True)
# :art: **ROW 4: Data Table (Full Width)**
st.subheader(":clipboard: Credit Usage Details by Warehouse")
st.dataframe(credits_data)
# Footer
st.markdown("---")
st.markdown("<p style='text-align:center;'>Built with :heart: using <b>Streamlit</b>, <b>Pandas</b>, <b>Altair</b>, and <b>Plotly</b></p>", unsafe_allow_html=True)