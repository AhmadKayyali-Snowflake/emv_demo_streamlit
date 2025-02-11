import streamlit as st
from snowflake.snowpark import Session

# Get the current credentials
st.title("Credit Usage 💰")

session = Session.builder.config("connection_name", "my_conn").create()

st.write(session.sql("""
SELECT 
SUM(CREDITS_USED) AS TOTAL_CREDITS_USED
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY;
                     """).collect())

