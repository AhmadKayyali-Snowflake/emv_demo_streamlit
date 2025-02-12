import streamlit as st

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