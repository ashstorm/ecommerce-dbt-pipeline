from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine, text

# --- Default settings for all tasks ---
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# --- The function that loads raw data ---
def load_raw_data():
    engine = create_engine(
        "postgresql://postgres:postgres@host.docker.internal:5432/ecommerce_db"
    )

    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
        print("Raw schema ready")

    tables = {
        "raw_orders":            "olist_orders_dataset.csv",
        "raw_customers":         "olist_customers_dataset.csv",
        "raw_order_items":       "olist_order_items_dataset.csv",
        "raw_payments":          "olist_order_payments_dataset.csv",
        "raw_products":          "olist_products_dataset.csv",
        "raw_reviews":           "olist_order_reviews_dataset.csv",
        "raw_sellers":           "olist_sellers_dataset.csv",
        "raw_name_translations": "product_category_name_translation.csv",
    }

    for table, file in tables.items():
        try:
            df = pd.read_csv(f"/opt/airflow/data/{file}")
            with engine.begin() as conn:
                conn.execute(text(f"TRUNCATE TABLE raw.{table};"))
            df.to_sql(table, engine, schema="raw", if_exists="append", index=False)
            print(f"Loaded {table} — {len(df)} rows")
        except Exception as e:
            print(f"Failed to load {table}: {e}")
            raise e

# --- Define the DAG ---
with DAG(
    dag_id="ecommerce_pipeline",
    default_args=default_args,
    description="E-Commerce ELT Pipeline",
    schedule_interval="0 8 * * *",  # runs every day at 8am
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    # Task 1 — Load raw data
    task_load_raw = PythonOperator(
        task_id="load_raw_data",
        python_callable=load_raw_data,
    )

    # Task 2 — Run dbt staging
    task_dbt_staging = BashOperator(
        task_id="run_dbt_staging",
        bash_command="cd /opt/airflow/dbt/ecommerce_dbt && /home/airflow/.local/bin/dbt run --select staging --profiles-dir /home/airflow/.dbt",
    )

    # Task 3 — Run dbt intermediate
    task_dbt_intermediate = BashOperator(
        task_id="run_dbt_intermediate",
        bash_command="cd /opt/airflow/dbt/ecommerce_dbt && /home/airflow/.local/bin/dbt run --select intermediate --profiles-dir /home/airflow/.dbt",
    )

    # Task 4 — Run dbt marts
    task_dbt_marts = BashOperator(
        task_id="run_dbt_marts",
        bash_command="cd /opt/airflow/dbt/ecommerce_dbt && /home/airflow/.local/bin/dbt run --select marts --profiles-dir /home/airflow/.dbt",
    )

    # Task 5 — Run dbt tests
    task_dbt_tests = BashOperator(
        task_id="run_dbt_tests",
        bash_command="cd /opt/airflow/dbt/ecommerce_dbt && /home/airflow/.local/bin/dbt test --profiles-dir /home/airflow/.dbt",
    )

    # --- Define the order ---
    task_load_raw >> task_dbt_staging >> task_dbt_intermediate >> task_dbt_marts >> task_dbt_tests