from functions.session import create_session
import pandas as pd

session = create_session()

def total_queries(database):
    return session.sql(f"""
       SELECT 
    DATABASE_NAME, 
    COUNT(*) AS TOTAL_QUERIES
    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
    WHERE DATABASE_NAME = '{database}'
    GROUP BY DATABASE_NAME
    ORDER BY TOTAL_QUERIES DESC;                
    """).to_pandas()

def total_credits(database):
    return session.sql(f"""
        WITH warehouse_sizes AS (
            SELECT 'X-Small' AS warehouse_size, 1 AS credits_per_hour UNION ALL
            SELECT 'Small' AS warehouse_size, 2 AS credits_per_hour UNION ALL
            SELECT 'Medium' AS warehouse_size, 4 AS credits_per_hour UNION ALL
            SELECT 'Large' AS warehouse_size, 8 AS credits_per_hour UNION ALL
            SELECT 'X-Large' AS warehouse_size, 16 AS credits_per_hour UNION ALL
            SELECT '2X-Large' AS warehouse_size, 32 AS credits_per_hour UNION ALL
            SELECT '3X-Large' AS warehouse_size, 64 AS credits_per_hour UNION ALL
            SELECT '4X-Large' AS warehouse_size, 128 AS credits_per_hour
        )
        SELECT
            qh.database_name,
            ROUND(SUM(qh.execution_time / (1000 * 60 * 60) * wh.credits_per_hour),2) AS total_query_cost
        FROM snowflake.account_usage.query_history AS qh
        INNER JOIN warehouse_sizes AS wh
            ON qh.warehouse_size=wh.warehouse_size
        WHERE qh.DATABASE_NAME = '{database}'
        GROUP BY qh.database_name
        ORDER BY total_query_cost DESC;             
    """).to_pandas()


def unique_users(database):
    return session.sql(f"""
    SELECT COUNT(DISTINCT USER_NAME) AS total_unique_users
    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY              
    WHERE DATABASE_NAME = '{database}'
    """).to_pandas()


def successful_queries(database):
    return session.sql(f"""
    SELECT COUNT(*) AS successful_queries
    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
    WHERE DATABASE_NAME = '{database}'
    AND ERROR_CODE IS NULL            
    """).to_pandas()

def failed_queries(database):
    return session.sql(f"""
    SELECT COUNT(*) AS failed_queries
    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
    WHERE DATABASE_NAME = '{database}'
    AND ERROR_CODE IS NOT NULL            
    """).to_pandas()

def queries_per_day(database):
    return session.sql(f"""
    SELECT 
    DATE_TRUNC('DAY', START_TIME) AS query_date,
    COUNT(*) AS queries_count
    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
    WHERE DATABASE_NAME = '{database}'
    GROUP BY query_date
    ORDER BY query_date;         
    """).to_pandas()



def unique_users_per_day(database):
    return session.sql(f"""
    SELECT 
        DATE_TRUNC('DAY', START_TIME) AS query_date,
        COUNT(DISTINCT USER_NAME) AS unique_users
    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
    WHERE DATABASE_NAME = '{database}'
    GROUP BY query_date
    ORDER BY query_date;         
    """).to_pandas()
