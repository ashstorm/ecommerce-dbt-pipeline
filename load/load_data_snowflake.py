import pandas as pd
from sqlalchemy import create_engine, text
from snowflake.sqlalchemy import URL
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Snowflake connection
engine = create_engine(URL(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    role=os.getenv("SNOWFLAKE_ROLE")
))

# Tables to load
tables= {
    "raw_customers":    "olist_customers_dataset.csv",
    "raw_order_items":  "olist_order_items_dataset.csv",
    "raw_payments":   "olist_order_payments_dataset.csv",
    "raw_reviews":    "olist_order_reviews_dataset.csv",
    "raw_orders":   "olist_orders_dataset.csv",
    "raw_products": "olist_products_dataset.csv",
    "raw_sellers":  "olist_sellers_dataset.csv",
    "raw_name_translations": "product_category_name_translation.csv",
}

# Load each file
for table, file in tables.items():
    try:
        df = pd.read_csv(f"../data/{file}")
        df.columns = df.columns.str.lower()
        df.to_sql(
            table.upper(),
            engine,
            schema="raw",
            if_exists="replace",
            index=False,
            chunksize=1000
        )
        print(f"Loaded {table} — {len(df)} rows")
    except Exception as e:
        print(f"Failed to load {table}: {e}")

print("\ndone")