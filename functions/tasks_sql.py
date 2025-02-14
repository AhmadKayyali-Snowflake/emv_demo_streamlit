from functions.session import create_session
import pandas as pd
import streamlit as st

session = create_session()

@st.cache_data
def tasks_by_refresh_status():
    return session.sql("""
    SELECT 
        STATE AS REFRESH_STATUS, 
        COUNT(*) AS TASK_COUNT
    FROM SNOWFLAKE.ACCOUNT_USAGE.TASK_HISTORY
    GROUP BY STATE
    ORDER BY TASK_COUNT DESC;
    """).to_pandas()

@st.cache_data
def max_task_lag_difference():
    result = session.sql("""
    SELECT
    NAME AS TASK_NAME,
    DATEDIFF(SECOND, SCHEDULED_TIME, QUERY_START_TIME) AS MAX_LAG_DIFFERENCE_SECONDS
    FROM SNOWFLAKE.ACCOUNT_USAGE.TASK_HISTORY
    WHERE QUERY_START_TIME > SCHEDULED_TIME
    ORDER BY MAX_LAG_DIFFERENCE_SECONDS DESC
    LIMIT 1;
    """).collect()
    return result[0]["MAX_LAG_DIFFERENCE_SECONDS"] if result else 0

@st.cache_data
def failed_tasks_last_24_hours():
    return session.sql("""
    SELECT 
        NAME AS TASK_NAME, 
        STATE, 
        ERROR_MESSAGE, 
        SCHEDULED_TIME, 
        COMPLETED_TIME
    FROM SNOWFLAKE.ACCOUNT_USAGE.TASK_HISTORY
    WHERE (STATE = 'FAILED' OR STATE = 'FAILED_AND_AUTO_SUSPENDED')
    AND SCHEDULED_TIME >= DATEADD(HOUR, -24, CURRENT_TIMESTAMP)
    ORDER BY SCHEDULED_TIME DESC;
    """).to_pandas()

@st.cache_data
def dynamic_tables_by_refresh_status():
    """Returns the count of tasks grouped by their execution state."""
    return session.sql("""
    SELECT 
        STATE AS REFRESH_STATUS, 
        COUNT(*) AS DYNAMIC_TABLE_COUNT
    FROM SNOWFLAKE.ACCOUNT_USAGE.DYNAMIC_TABLE_REFRESH_HISTORY
    GROUP BY STATE
    ORDER BY DYNAMIC_TABLE_COUNT DESC;
    """).to_pandas()

@st.cache_data
def max_dynamic_tables_lag_difference():
    result = session.sql("""
    SELECT 
        QUALIFIED_NAME, 
        DATA_TIMESTAMP, 
        REFRESH_END_TIME, 
        TARGET_LAG_SEC, 
        COMPLETION_TARGET,
        DATEDIFF(SECOND, DATA_TIMESTAMP, REFRESH_END_TIME) AS ACTUAL_LAG_SEC, 
        ACTUAL_LAG_SEC - TARGET_LAG_SEC AS MAX_LAG_DIFFERENCE_SECONDS
    FROM SNOWFLAKE.ACCOUNT_USAGE.DYNAMIC_TABLE_REFRESH_HISTORY
    WHERE ACTUAL_LAG_SEC > TARGET_LAG_SEC
    ORDER BY MAX_LAG_DIFFERENCE_SECONDS DESC
    LIMIT 1;
    """).collect()
    return result[0]["MAX_LAG_DIFFERENCE_SECONDS"] if result else 0

@st.cache_data
def failed_dynamic_tables_last_24_hours():
    return session.sql("""
    SELECT 
    NAME AS TASK_NAME, 
    STATE, 
    STATE_MESSAGE, 
    REFRESH_END_TIME, 
    FROM SNOWFLAKE.ACCOUNT_USAGE.DYNAMIC_TABLE_REFRESH_HISTORY
    WHERE (STATE = 'FAILED' OR STATE = 'UPSTREAM_FAILED')
    AND REFRESH_END_TIME >= DATEADD(HOUR, -24, CURRENT_TIMESTAMP)
    ORDER BY REFRESH_END_TIME DESC;
    """).to_pandas()