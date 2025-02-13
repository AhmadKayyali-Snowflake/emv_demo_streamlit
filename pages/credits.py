import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from functions.credits_sql import *

# --- FETCH DATA ---
total_used = credits_used()
total_remaining = credits_remaining()
percentage_used = percentage_credits_used()
df_warehouse = credits_per_warehouse()


st.title("💰 Credits Usage Dashboard")
st.write("")
credit_usage= st.columns(3)
credit_usage[0].metric(label="Total Credits Used", value=f"{total_used:.2f}")
credit_usage[1].metric(label="% of Credits Used", value=f"{percentage_used:.2f}%")
credit_usage[2].metric(label="Total Credits Remaining", value=f"{total_remaining:.2f}")
# Divider
st.markdown("---")



# --- CREATE COLUMNS ---
col1, col2 = st.columns((3, 6))

# === COLUMN 1: DONUT CHARTS ===
with col1:
    # Pie Chart: Total Credits Used
    fig_used = px.pie(
        names=["Used", "Unused"],
        values=[total_used, total_remaining],
        hole=0.6,
        title="Total Credit Usage",
        color_discrete_sequence=["#2ECC71", "#E74C3C"]
    )
    fig_used.add_annotation(
        text=f"{total_used:,.2f}",
        x=0.5, y=0.5,
        font=dict(size=24, color="white"),
        showarrow=False,
    )
    fig_used.update_layout(showlegend=False)  
    st.plotly_chart(fig_used, use_container_width=True)

    warehouse_credits = credits_by_warehouse()
    chart = alt.Chart(warehouse_credits).mark_bar(color="steelblue").encode(
        x="Warehouse",
        y="Credits",
        tooltip=["Warehouse", "Credits"]
    ).properties(
        title="Credit Usage by Warehouse",
        width="container",
        height=500  # Adjust height as needed (e.g., 600px or more)
    ).configure_view(
        stroke=None  # Removes unnecessary borders to make it more fluid
    )

    st.altair_chart(chart, use_container_width=True)

    

# === COLUMN 2: BAR CHART (CREDITS OVER TIME) ===
with col2:
    df_monthly_warehouse = credits_used_per_month_by_warehouse()

    fig_bar = px.bar(
        df_monthly_warehouse,
        title="Monthly Credit Usage by Warehouse",
        x="Month",
        y="Credits",
        color="Warehouse",
        barmode="stack",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig_bar.update_layout(
        xaxis_title="Month",
        yaxis_title="Credits",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, zeroline=False),
        hovermode="x unified",
        showlegend=False
    )

    st.plotly_chart(fig_bar, use_container_width=True)


    monthly_credit_usage = credits_per_month()
    fig_line = px.line(
        monthly_credit_usage,
        x="Month",
        y="Credits",
        markers=True,
        title="Monthly Credit Consumption",
        line_shape="spline",
        color_discrete_sequence=["#2E86C1"]
    )
    st.plotly_chart(fig_line, use_container_width=True)