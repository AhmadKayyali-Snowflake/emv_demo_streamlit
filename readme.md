# EMV Credit and Query Metric POC

## Overview

This Streamlit app is an analytics platform designed to monitor and optimize performance in Snowflake. Gain insights into queries, tasks, dynamic tables, credits, and data feeds with real-time visualizations.

## Prerequisites
1. Before following the steps below you must have a snow cli connection set up.
If you have not done this already, please navigate to the [Snowflake CLI Configuration](https://docs.snowflake.com/en/developer-guide/snowflake-cli/connecting/configure-connections#add-a-connection) page and follow the steps.
Once you have successfully set up and tested your connection, you may continue.

## Setup Instructions

### Step 1 - Activate Conda Environment & Virtual Environment

1. Ensure you have [Anaconda](https://www.anaconda.com/) installed.
2. Create a new Conda environment if you have not done so already.
3. Ensure you are in your project directory:
   ```bash
   cd path/to/project
   ```
4. Activate the environment by running:
   ```bash
   conda activate myenv
   ```
5. Create and activate a virtual environment inside the Conda environment by running:
   ```bash
   python3.11 -m venv venv
   ```
   - On Windows, run:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux, run:
     ```bash
     source venv/bin/activate
     ```

### Step 2 - Install Dependencies for Local Development

1. Ensure you are using python 3.11 by running the following command:
   ```bash
   python —version
   ```
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Step 3 - Start Streamlit App Locally

1. Test your Snowflake connection before starting the app:
   ```bash
   snow connection test --connection my_conn
   ```
2. Navigate to the "functions" folder and open the `session.py` file.
   - Modify the following line of code on **line 11**:
      ```python
      session = Session.builder.config("connection_name", "my_conn").create()
      ```
      Replace `"my_conn"` with the actual name of your Snowflake CLI connection. To find your connection name, run:
      ```bash
      snow connection list
      ```
4. Start the Streamlit app by running:
   ```bash
   streamlit run Home.py
   ```
5. Open the provided URL in your browser to interact with the app.

### Step 4 - Deploy Streamlit App Using Snow CLI

1. Navigate to the `snowflake.yml` file in the root of the project and update the database and schema under the identifier section.
2. Deploy the app:
   - If deploying for the first time:
     ```bash
     snow streamlit deploy --database <your_database> --schema <your_schema>
     ```
   - If replacing an existing deployment:
     ```bash
     snow streamlit deploy --replace --database <your_database> --schema <your_schema>
     ```
3. For documentation on `snow streamlit deploy`, visit:
   [Snowflake CLI Documentation](https://docs.snowflake.com/en/developer-guide/snowflake-cli/command-reference/streamlit-commands/deploy)

## Project Breakdown

### `Home.py`

Landing page and root of the app.

### `snowflake.yml`

Project definition file for the Streamlit app. It specifies files for deployment, the Snowflake warehouse hosting the app, and more.
Learn more about this file structure in the [Snowflake Documentation](https://docs.snowflake.com/en/developer-guide/snowflake-cli/streamlit-apps/manage-apps/initialize-app#label-snowcli-streamlit-project-definition).

### `environment.yml`

Specifies dependencies required by the Streamlit app.

### `Pages/`

Each file contains code for each page of the app.

## Dashboards and Metrics

### **Credit Usage Dashboard**

**Purpose:** Provides an overview of credit usage in Snowflake to help users monitor their credit consumption.

**Metrics Available:**

- Total Credits Used
- Percentage of Credits Used
- Total Credits Remaining
- Monthly Credits by Warehouse
- Credit Usage by Warehouse
- Monthly Credit Consumption
- Estimated Credit Consumption Per Query

### **Data Feeds Dashboard**

**Purpose:** Monitors query success rates, credit usage, and unique users in a Snowflake database.

**Metrics Available:**

- Total Successful Queries
- Total Failed Queries
- Total Queries
- Total Credits Used
- Unique Users
- Queries Per Day
- Unique Users Per Day

### **Query Monitoring Dashboard**

**Purpose:** Tracks query execution performance, including query statuses, failures, and execution trends.

**Metrics Available:**

- Max Query Duration (Minutes)
- Failed Queries (Last 24 Hours)
- Total Queries Executed
- Query Volume by Status
- Queries by User
- Longest Queries (Last 24 Hours)

### **Task & Dynamic Table Execution Dashboard**

**Purpose:** Monitors task execution and dynamic table metrics, including lag times, failures, and performance.

**Metrics Available:**

- Max Task & Dynamic Table Execution Lag
- Execution Volume by Status
- Failed Tasks & Dynamic Tables

### **Functions Folder**

Contains SQL queries for each dashboard.

- The only exception is `session.py`, which sets up the Snowflake connection.