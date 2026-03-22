import pandas as pd
from sqlalchemy import create_engine, text
from snowflake.sqlalchemy import URL

# Snowflake connection
engine = create_engine(URL(
    account="DDJFEQH-XCC20271",
    user="asharma",
    password="WciuzKVN9CY7tab",
    database="ecommerce_db",
    schema="RAW",
    warehouse="ecommerce_wh",
    role="ACCOUNTADMIN"
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