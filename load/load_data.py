import pandas as pd
from sqlalchemy import create_engine, text

#connecting to docker postgres
engine = create_engine("postgresql://postgres:postgres@localhost:5432/ecommerce_db")

#creating raw schema
with engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
    conn.commit()
    print("The schema is ready m'lord")

#loading tables and mapping em in a dictionary
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

#load files with a try except
for table, file in tables.items():
    try:
        df=pd.read_csv(f"../data/{file}")
        df.to_sql(table, engine, schema="raw", if_exists="replace", index=False)
        print(f"We have loaded {table} that has {len(df)} rows")
    except Exception as shi:
        print(f"We have failed to load {table} because of {shi}")

#and this should be good for now
print("Done")