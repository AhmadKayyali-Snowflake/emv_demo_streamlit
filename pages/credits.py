import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from functions.credits_sql import *

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Credit Usage",
    layout="wide",
    initial_sidebar_state="expanded"
)

alt.themes.enable("dark")

# --- FETCH DATA ---
total_used = credits_used()
total_remaining = credits_remaining()
percentage_used = percentage_credits_used()

# Fetch warehouse credits data
df_warehouse = credits_per_warehouse()

# --- CREATE COLUMNS ---
col1, col2, col3 = st.columns((1.5, 6, 2.5))

# === COLUMN 1: DONUT CHARTS ===
with col1:
    with st.container():
        st.markdown("#### Credit Usage")

        # Pie Chart: Total Credits Used
        fig_used = px.pie(
            names=["Used", "Unused"],
            values=[total_used, total_remaining],
            hole=0.6,
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

# === COLUMN 2: BAR CHART (CREDITS OVER TIME) ===
with col2:
    st.markdown("#### Monthly Credit Usage by Warehouse")

    df_monthly_warehouse = credits_used_per_month_by_warehouse()

    fig_bar = px.bar(
        df_monthly_warehouse,
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

    # Display Bar Chart
    st.plotly_chart(fig_bar, use_container_width=True)

with col3:
    st.markdown("#### Total Warehouse Credit Usage")
    # Display DataFrame with a Progress Bar Column
    st.dataframe(
        data = df_warehouse,
        hide_index=True
    )

