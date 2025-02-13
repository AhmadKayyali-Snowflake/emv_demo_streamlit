# queries_sql.py
from functions.session import create_session
import pandas as pd

session = create_session()

def queries_by_user():
    """Returns the total number of queries executed by each user."""
    return session.sql("""
        SELECT USER_NAME, COUNT(QUERY_ID) AS TOTAL_QUERIES
        FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
        GROUP BY USER_NAME
        ORDER BY TOTAL_QUERIES DESC;
    """).to_pandas()

def query_volume_by_status():
    """Returns the count of queries grouped by status."""
    return session.sql("""
        SELECT EXECUTION_STATUS, COUNT(QUERY_ID) AS QUERY_COUNT
        FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
        GROUP BY EXECUTION_STATUS
        ORDER BY QUERY_COUNT DESC;
    """).to_pandas()

def failed_queries_last_24_hours():
    """Returns a list of failed queries executed in the last 24 hours."""
    return session.sql("""
        SELECT QUERY_ID, USER_NAME, START_TIME, ERROR_MESSAGE
        FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
        WHERE EXECUTION_STATUS = 'FAILED'
        AND START_TIME >= DATEADD(HOUR, -24, CURRENT_TIMESTAMP())
        ORDER BY START_TIME DESC;
    """).to_pandas()

def max_query_duration():
    """Returns the maximum query duration recorded in seconds."""
    result = session.sql("""
        SELECT MAX(TOTAL_ELAPSED_TIME) AS MAX_QUERY_DURATION
        FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY;
    """).collect()
    return result[0]["MAX_QUERY_DURATION"] if result else 0

def longest_queries_last_24_hours():
    """Returns the list of queries with the highest duration in the last 24 hours."""
    return session.sql("""
        SELECT QUERY_ID, USER_NAME, START_TIME, TOTAL_ELAPSED_TIME AS DURATION
        FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
        WHERE START_TIME >= DATEADD(HOUR, -24, CURRENT_TIMESTAMP())
        ORDER BY DURATION DESC
        LIMIT 10;
    """).to_pandas()
