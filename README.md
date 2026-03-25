# E-Commerce Analytics Pipeline

## Overview
An end-to-end ELT pipeline built on the Brazilian E-Commerce 
(Olist) dataset, processing 100,000+ records through a 
multi-layer dbt project, orchestrated with Apache Airflow 
and hosted on Snowflake.

## Architecture
Raw Data (Kaggle CSVs)
↓
Python + SQLAlchemy (Ingestion)
↓
PostgreSQL / Snowflake (Warehouse)
↓
dbt Core (Transformation)
├── Staging Layer    → clean & rename
├── Intermediate     → join tables
└── Marts            → business ready
↓
Apache Airflow (Orchestration)
↓
Apache Superset (BI Dashboard)
## Tech Stack
| Tool | Purpose |
|---|---|
| Python | Data ingestion |
| PostgreSQL | Local data warehouse |
| Snowflake | Cloud data warehouse |
| dbt Core | Data transformation |
| Apache Airflow | Pipeline orchestration |
| Apache Superset | BI dashboard |
| Docker | Containerisation |
| SQLAlchemy | Database connection |

## dbt Models
### Staging (6 models)
- `stg_orders` — cleaned order data with proper timestamps
- `stg_customers` — cleaned customer data
- `stg_payments` — cleaned payment data
- `stg_products` — cleaned product data
- `stg_sellers` — cleaned seller data
- `stg_reviews` — cleaned review data

### Intermediate (3 models)
- `int_orders_with_payments` — orders + payment totals
- `int_orders_with_customers` — orders + customer details
- `int_products_with_categories` — products + English 
   category names

### Marts (3 models)
- `mart_monthly_revenue` — monthly revenue trends
- `mart_customer_segments` — customers by spend tier
- `mart_delivery_performance` — delivery times by state

## Data Quality
15 dbt tests covering:
- Uniqueness checks
- Not null checks
- Accepted value validation

## Airflow DAG
Daily pipeline at 8am:
1. Load raw data into Snowflake
2. Run dbt staging models
3. Run dbt intermediate models
4. Run dbt mart models
5. Run dbt tests

## Dashboard
Apache Superset dashboard with 3 charts:
- Monthly Orders Trend
- Delivery Performance by State
- Customer Segmentation

## How to Run

### Prerequisites
- Docker Desktop
- Python 3.8+
- Snowflake account
- dbt-snowflake

### Setup
1. Clone the repo
   ```bash
   git clone https://github.com/ashstorm/ecommerce-dbt-pipeline
   cd ecommerce-dbt-pipeline
Create a .env file using .env.example as template
cp .env.example .env
Load raw data
cd load
python load_data_snowflake.py
Run dbt models
cd ecommerce_dbt
dbt run
dbt test
Start Airflow
cd airflow
docker-compose up -d
Start Superset
cd superset
docker-compose up -d
Dataset
Brazilian E-Commerce dataset by Olist —
available on Kaggle:
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
