import streamlit as st
import pandas as pd
import plotly.express as px
from functions.queries_sql import *

st.set_page_config(
    layout="wide",
    page_icon="📈"
)

# --- FETCH DATA ---
df_queries_by_user = queries_by_user()
df_query_status = query_volume_by_status()
df_failed_queries = failed_queries_last_24_hours()
max_duration = max_query_duration()
df_longest_queries = longest_queries_last_24_hours()

# --- HEADER ---
st.title("📈 Query Analysis Dashboard")
st.markdown("An interactive **real-time** overview of query execution, failures, and user activity.")

# --- PERFORMANCE METRICS ---
st.markdown("### ⏳ Performance Overview")
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Max Query Duration (s)", value=f"{max_duration:.2f}", delta_color="inverse")

with col2:
    st.write("📝 **Tip:** Use tabs below to navigate and explore detailed query insights.")

st.markdown("---")

# --- TABS FOR NAVIGATION ---
tab1, tab2, tab3 = st.tabs(["📊 Query Status", "👤 Queries by User", "❌ Failed Queries"])

# --- TAB 1: QUERY STATUS ---
with tab1:
    col1, col2 = st.columns((5, 5))

    with col1:
        st.subheader("✅ Query Volume by Status")

        # Assign colors manually for better distinction
        status_colors = {
            "SUCCESS": "#2ECC71",  # Green
            "FAILED": "#E74C3C",  # Red
            "OTHER": "#F39C12"  # Yellow/Orange
        }

        # Add a new color column for consistent coloring
        df_query_status["COLOR"] = df_query_status["EXECUTION_STATUS"].map(status_colors)

        fig_status = px.pie(
            df_query_status,
            names="EXECUTION_STATUS",
            values="QUERY_COUNT",
            hole=0.4,  # Donut Chart Effect
            title="Query Volume by Execution Status",
            color="EXECUTION_STATUS",
            color_discrete_map=status_colors
        )
        st.plotly_chart(fig_status, use_container_width=True)

    with col2:
        st.subheader("⏳ Longest Queries in the Last 24 Hours")
        st.data_editor(
            df_longest_queries,
            use_container_width=True,
            height=250,
            hide_index=True
        )

# --- TAB 2: QUERIES BY USER ---
with tab2:
    st.subheader("👤 Queries Executed by User")

    # Dropdown Filter
    user_list = df_queries_by_user["USER_NAME"].unique()
    selected_user = st.selectbox("Filter by User:", ["All"] + list(user_list))
    
    # Filter Data
    if selected_user != "All":
        df_filtered_users = df_queries_by_user[df_queries_by_user["USER_NAME"] == selected_user]
    else:
        df_filtered_users = df_queries_by_user

    # Bar Chart
    fig_users = px.bar(
        df_filtered_users,
        x="TOTAL_QUERIES",
        y="USER_NAME",
        title="Queries Executed by User",
        orientation="h",
        color="TOTAL_QUERIES",
        color_continuous_scale="blues"
    )
    st.plotly_chart(fig_users, use_container_width=True)

# --- TAB 3: FAILED QUERIES ---
with tab3:
    st.subheader("❌ Failed Queries in the Last 24 Hours")
    st.data_editor(
        df_failed_queries,
        use_container_width=True,
        height=250,
        hide_index=True
    )
