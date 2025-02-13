# tasks_sql.py
from functions.session import create_session
import pandas as pd

session = create_session()

def tasks_by_refresh_status():
    """Returns the count of tasks grouped by their execution state."""
    return session.sql("""
        SELECT STATE, COUNT(*) AS COUNT
        FROM SNOWFLAKE.ACCOUNT_USAGE.TASK_HISTORY
        GROUP BY STATE
        ORDER BY COUNT DESC;
    """).to_pandas()

def max_task_lag_difference():
    """Returns the maximum execution time difference between scheduled and completed time."""
    return session.sql("""
        SELECT MAX(DATEDIFF(SECOND, SCHEDULED_TIME, COMPLETED_TIME)) AS MAX_EXECUTION_LAG
        FROM SNOWFLAKE.ACCOUNT_USAGE.TASK_HISTORY;
    """).collect()[0]["MAX_EXECUTION_LAG"]

def failed_tasks_last_24_hours():
    """Returns a list of failed tasks executed in the last 24 hours."""
    return session.sql("""
        SELECT 
            NAME AS Task_Name,
            DATABASE_NAME AS Database,
            SCHEMA_NAME AS Schema,
            STATE AS Status,
            ERROR_MESSAGE AS Error,
            SCHEDULED_TIME AS Last_Failure_Time
        FROM SNOWFLAKE.ACCOUNT_USAGE.TASK_HISTORY
        WHERE STATE = 'FAILED'
        AND SCHEDULED_TIME >= DATEADD(HOUR, -24, CURRENT_TIMESTAMP)
        ORDER BY SCHEDULED_TIME DESC;
    """).to_pandas()
