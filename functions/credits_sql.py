from functions.session import create_session
import pandas as pd

session = create_session()

def credits_used():
    total_credits_used = session.sql("""
        SELECT ROUND(SUM(CREDITS_USED),2) AS TOTAL_CREDITS_USED
        FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY;
    """).collect()[0]["TOTAL_CREDITS_USED"]

    return total_credits_used if total_credits_used else 0

def credits_remaining():
    credits_remaining = session.sql("""
        SELECT ROUND(1000 - SUM(CREDITS_USED),2) AS CREDITS_REMAINING
        FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
    """).collect()[0]["CREDITS_REMAINING"]

    return credits_remaining if credits_remaining else 0

def percentage_credits_used():
    percentage_of_credits_used = session.sql("""
        SELECT 
        ROUND(SUM(CREDITS_USED) / 1000 * 100, 2) AS PERCENTAGE_CREDITS_USED
        FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY;
    """).collect()[0]["PERCENTAGE_CREDITS_USED"]

    return percentage_of_credits_used if percentage_of_credits_used else 0

def credits_used_per_month_by_warehouse():
    total_credits_used_month_warehouse = session.sql("""
        SELECT 
        TO_CHAR(DATE_TRUNC('MONTH', START_TIME), 'YYYY-MM') AS MONTH, 
        WAREHOUSE_NAME AS WAREHOUSE,
        SUM(CREDITS_USED) AS TOTAL_CREDITS_USED
        FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
        GROUP BY MONTH, WAREHOUSE
        ORDER BY MONTH DESC;
    """).to_pandas()

    total_credits_used_month_warehouse.rename(columns={"MONTH": "Month", "TOTAL_CREDITS_USED": "Credits", "WAREHOUSE": "Warehouse"}, inplace=True)
    
    total_credits_used_month_warehouse["Month"] = pd.to_datetime(total_credits_used_month_warehouse["Month"])

    return total_credits_used_month_warehouse


def credits_by_warehouse():
    total_by_warehouse = session.sql("""
        SELECT 
        WAREHOUSE_NAME AS WAREHOUSE,
        ROUND(SUM(CREDITS_USED),0) AS TOTAL_CREDITS_USED
        FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
        GROUP BY WAREHOUSE
        ORDER BY WAREHOUSE DESC;
    """).to_pandas()

    total_by_warehouse.rename(columns={"WAREHOUSE": "Warehouse", "TOTAL_CREDITS_USED": "Credits"}, inplace=True)
    
    return total_by_warehouse

def credits_per_month():
    total_credits_used_month = session.sql("""
    SELECT 
        TO_CHAR(DATE_TRUNC('MONTH', START_TIME), 'YYYY-MM') AS MONTH, 
        SUM(CREDITS_USED) AS TOTAL_CREDITS_USED,
        SUM(CREDITS_USED) - LAG(SUM(CREDITS_USED)) OVER (ORDER BY DATE_TRUNC('MONTH', START_TIME)) AS MOM_CHANGE,
        ROUND(
            (SUM(CREDITS_USED) - LAG(SUM(CREDITS_USED)) OVER (ORDER BY DATE_TRUNC('MONTH', START_TIME))) /
            NULLIF(LAG(SUM(CREDITS_USED)) OVER (ORDER BY DATE_TRUNC('MONTH', START_TIME)), 0) * 100, 
            2
        ) AS PERCENT_CHANGE
    FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
    GROUP BY DATE_TRUNC('MONTH', START_TIME)
    ORDER BY MONTH DESC;
    """).to_pandas()

    total_credits_used_month.rename(columns={"MONTH": "Month", "TOTAL_CREDITS_USED": "Credits", "MOM_CHANGE": "MOM Change", "PERCENT_CHANGE": "Percentage Change"}, inplace=True)
    
    total_credits_used_month["Month"] = pd.to_datetime(total_credits_used_month["Month"])

    return total_credits_used_month

def credits_per_warehouse():
    credits_per_warehouse = session.sql("""
    SELECT 
    WAREHOUSE_NAME, 
    SUM(CREDITS_USED) AS TOTAL_CREDITS_USED
    FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
    GROUP BY WAREHOUSE_NAME
    ORDER BY TOTAL_CREDITS_USED DESC;
    """).to_pandas()

    credits_per_warehouse.rename(columns={"WAREHOUSE_NAME": "Warehouse", "TOTAL_CREDITS_USED": "Credits"}, inplace=True)

    return credits_per_warehouse

def credits_per_query():
    return session.sql("""
        WITH
    warehouse_sizes AS (
        SELECT 'X-Small' AS warehouse_size, 1 AS credits_per_hour UNION ALL
        SELECT 'Small' AS warehouse_size, 2 AS credits_per_hour UNION ALL
        SELECT 'Medium'  AS warehouse_size, 4 AS credits_per_hour UNION ALL
        SELECT 'Large' AS warehouse_size, 8 AS credits_per_hour UNION ALL
        SELECT 'X-Large' AS warehouse_size, 16 AS credits_per_hour UNION ALL
        SELECT '2X-Large' AS warehouse_size, 32 AS credits_per_hour UNION ALL
        SELECT '3X-Large' AS warehouse_size, 64 AS credits_per_hour UNION ALL
        SELECT '4X-Large' AS warehouse_size, 128 AS credits_per_hour
    )
    SELECT
        qh.user_name,
        qh.execution_time/(1000*60*60)*wh.credits_per_hour AS query_cost,
        ROUND(qh.total_elapsed_time / 1000 / 60, 2) AS duration_minutes,
        qh.warehouse_name,
        qh.warehouse_size,
        qh.start_time,
        qh.query_text,
        qh.query_id
    FROM snowflake.account_usage.query_history AS qh
    INNER JOIN warehouse_sizes AS wh
        ON qh.warehouse_size=wh.warehouse_size
    ORDER BY query_cost DESC
    LIMIT 50              
    """).to_pandas()  # Convert to Pandas DataFrame