from functions.session import create_session
import pandas as pd

session = create_session()

def credits_used():
    total_credits_used = session.sql("""
        SELECT SUM(CREDITS_USED) AS TOTAL_CREDITS_USED
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
    total_credits_used_month = session.sql("""
        SELECT 
        TO_CHAR(DATE_TRUNC('MONTH', START_TIME), 'YYYY-MM') AS MONTH, 
        WAREHOUSE_NAME AS WAREHOUSE,
        SUM(CREDITS_USED) AS TOTAL_CREDITS_USED
        FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
        GROUP BY MONTH, WAREHOUSE
        ORDER BY MONTH DESC;
    """).collect()

    months = [row["MONTH"] for row in total_credits_used_month]
    warehouse = [row["WAREHOUSE"] for row in total_credits_used_month]
    credits_used = [row["TOTAL_CREDITS_USED"] for row in total_credits_used_month]

    df = pd.DataFrame(list(zip(months, warehouse, credits_used)), columns=["Month", "Warehouse", "Credits"])

    df["Month"] = pd.to_datetime(df["Month"])

    return df


def credits_by_warehouse():
    total_credits_warehouse = session.sql("""
        SELECT 
        WAREHOUSE_NAME AS WAREHOUSE,
        ROUND(SUM(CREDITS_USED),0) AS TOTAL_CREDITS_USED
        FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
        GROUP BY WAREHOUSE
        ORDER BY WAREHOUSE DESC;
    """).collect()

    warehouse = [row["WAREHOUSE"] for row in total_credits_warehouse]
    credits_used = [row["TOTAL_CREDITS_USED"] for row in total_credits_warehouse]

    df = pd.DataFrame(list(zip(warehouse, credits_used)), columns=["Warehouse", "Credits"])
    return df

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
    """).collect()

    months = [row["MONTH"] for row in total_credits_used_month]
    credits_used = [row["TOTAL_CREDITS_USED"] for row in total_credits_used_month]
    mom_change = [row["MOM_CHANGE"] for row in total_credits_used_month]
    percentage_change = [row["PERCENT_CHANGE"] for row in total_credits_used_month]


    df = pd.DataFrame(list(zip(months, credits_used, mom_change, percentage_change)), columns=["Month", "Credits", "MOM Change", "Percentage Change"])
    
    df["Month"] = pd.to_datetime(df["Month"])

    return df

def credits_per_warehouse():
    credits_per_warehouse = session.sql("""
    SELECT 
    WAREHOUSE_NAME, 
    SUM(CREDITS_USED) AS TOTAL_CREDITS_USED
    FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
    GROUP BY WAREHOUSE_NAME
    ORDER BY TOTAL_CREDITS_USED DESC;
    """).collect()


    warehouse = [row["WAREHOUSE_NAME"] for row in credits_per_warehouse]
    credits_used = [row["TOTAL_CREDITS_USED"] for row in credits_per_warehouse]

    df = pd.DataFrame(list(zip(warehouse, credits_used)), columns=["Warehouse", "Credits"])
    return df
