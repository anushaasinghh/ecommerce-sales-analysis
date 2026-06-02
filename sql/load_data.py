import pandas as pd
import sqlite3
import os

# Connect to SQLite — this creates a file called ecommerce.db
conn = sqlite3.connect("ecommerce.db")

# List of all CSV files to load
csv_files = {
    "orders":          "data/olist_orders_dataset.csv",
    "order_items":     "data/olist_order_items_dataset.csv",
    "order_payments":  "data/olist_order_payments_dataset.csv",
    "products":        "data/olist_products_dataset.csv",
    "customers":       "data/olist_customers_dataset.csv",
    "sellers":         "data/olist_sellers_dataset.csv",
    "order_reviews":   "data/olist_order_reviews_dataset.csv",
    "category_translation": "data/product_category_name_translation.csv",
}

# Load each CSV into SQLite as a table
for table_name, filepath in csv_files.items():
    df = pd.read_csv(filepath)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"✅ Loaded {table_name} — {len(df):,} rows")

conn.close()
print("\n✅ Database created: ecommerce.db")