# E-Commerce Analytics Pipeline

## Overview
An end-to-end ELT pipeline built on the Brazilian E-Commerce (Olist) 
dataset, processing 100,000+ records through a multi-layer dbt project.

## Tech Stack
- Python — data extraction and loading
- PostgreSQL (Docker) — data warehouse
- dbt Core — data transformation
- SQLAlchemy — database connection

## Pipeline Architecture
Raw Data → Staging → Intermediate → Marts

## Models
### Staging
- stg_orders — cleaned order data with proper timestamps
- stg_customers — cleaned customer data
- stg_payments — cleaned payment data
- stg_products — cleaned product data
- stg_sellers — cleaned seller data
- stg_reviews — cleaned review data

### Intermediate
- int_orders_with_payments — orders joined with payment totals
- int_orders_with_customers — orders joined with customer details
- int_products_with_categories — products with English category names

### Marts
- mart_monthly_revenue — monthly revenue trends
- mart_customer_segments — customers segmented by spend
- mart_delivery_performance — delivery times by state

## Data Quality
15 dbt tests covering uniqueness, null checks, 
and accepted value validation.

## How to Run
1. Start PostgreSQL Docker container
2. Run `python load/load_data.py` to load raw data
3. Run `dbt run` to build all models
4. Run `dbt test` to validate data quality

## Airflow
+ Apache Airflow DAG running the full pipeline automatically every day
+ Automatic retries and error handling

## Snowflake
+ Migrated pipeline from PostgreSQL to Snowflake
