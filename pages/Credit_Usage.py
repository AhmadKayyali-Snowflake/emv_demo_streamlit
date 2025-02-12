import streamlit as st

# Get the current credentials
st.title("Credit Usage 💰")

@st.cache_resource
def create_session():
    try:
        from snowflake.snowpark import Session
        from snowflake.snowpark.context import get_active_session
        session = get_active_session()
    except:
        from snowflake.snowpark import Session
        session = Session.builder.config("connection_name", "my_conn").create()
    return session

session = create_session()
st.write(session.sql("""
SELECT 
SUM(CREDITS_USED) AS TOTAL_CREDITS_USED
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY;
                     """).collect())

