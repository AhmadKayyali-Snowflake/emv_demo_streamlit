import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from functions.credits_sql import *

total_used = credits_used()
total_remaining = credits_remaining()
percentage_used = percentage_credits_used()
df_warehouse = credits_per_warehouse()
df_monthly_warehouse = credits_used_per_month_by_warehouse()
monthly_credit_usage = credits_per_month()
warehouse_credits = credits_by_warehouse()



st.title("💰 Credits Usage Dashboard")
st.write("")
credit_usage = st.columns(3)
with credit_usage[0]:
    st.metric(label="Total Credits Used", value=f"{total_used:.2f}")

    mom_change = monthly_credit_usage['MOM Change'].iloc[0]
    mom_change = 0 if pd.isna(mom_change) else mom_change

    if mom_change > 0:
        st.markdown(f'<p style="font-weight:bold;">{mom_change:.2f} increase in credit usage since last month</p>', unsafe_allow_html=True)
    elif mom_change < 0:
        st.markdown(f'<p style="font-weight:bold;">{mom_change:.2f} decrease in credit usage since last month</p>', unsafe_allow_html=True)
    else: 
        st.write("<p style='font-weight:bold;'>No change in credit usage since last month</p>", unsafe_allow_html=True)

with credit_usage[1]:
    st.metric(label="% of Credits Used", value=f"{percentage_used:.2f}%")

    percentage_change = monthly_credit_usage['Percentage Change'].iloc[0]
    percentage_change = 0 if pd.isna(percentage_change) else percentage_change

    if percentage_change > 0:
        st.markdown(f'<p style="font-weight:bold;">{percentage_change:.2f}% increase in credit usage since last month</p>', unsafe_allow_html=True)
    elif percentage_change < 0:
        st.markdown(f'<p style="font-weight:bold;">{percentage_change:.2f}% decrease in rcredit usage since last month</p>', unsafe_allow_html=True)
    else: 
        st.write("<p style='font-weight:bold;'>No change in credit usage since last month</p>", unsafe_allow_html=True)

with credit_usage[2]:
    st.metric(label="Total Credits Remaining", value=f"{total_remaining:.2f}")


st.markdown("---")

df_monthly_warehouse["Month"] = df_monthly_warehouse["Month"].dt.strftime("%Y-%m")

# --- Generate Dynamic Warehouse Colors ---
unique_warehouses = df_monthly_warehouse["Warehouse"].unique().tolist()
color_palette = px.colors.qualitative.Set2  # Choose a predefined palette
warehouse_colors = {wh: color_palette[i % len(color_palette)] for i, wh in enumerate(unique_warehouses)}

col1, col2 = st.columns((3, 6))

with col1:
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
    
    chart = alt.Chart(warehouse_credits).mark_bar().encode(
        x="Warehouse",
        y="Credits",
        tooltip=["Warehouse", "Credits"],
        color=alt.Color(
        "Warehouse",
        scale=alt.Scale(domain=list(warehouse_colors.keys()), range=list(warehouse_colors.values())),
        legend=None  # Removes the legend
    )
    ).properties(
        title="Credit Usage by Warehouse",
        width="container",
        height=500,
    ).configure_view(stroke=None)



    st.altair_chart(chart, use_container_width=True)

with col2:
    fig_bar = px.bar(
        df_monthly_warehouse,
        title="Monthly Credit Usage by Warehouse",
        x="Month",
        y="Credits",
        color="Warehouse",
        barmode="stack",
        color_discrete_map=warehouse_colors
    )

    fig_bar.update_layout(
        xaxis_title="Month",
        yaxis_title="Credits",
        xaxis=dict(showgrid=False, type="category"),
        yaxis=dict(showgrid=True, zeroline=False),
        hovermode="x unified",
        showlegend=False
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    fig_line = px.line(
        monthly_credit_usage,
        x="Month",
        y="Credits",
        markers=True,
        title="Monthly Credit Consumption",
        line_shape="spline",
        color_discrete_sequence=["#2E86C1"],
    )
    st.plotly_chart(fig_line, use_container_width=True)