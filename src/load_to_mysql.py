import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# -----------------------------
# 1. CONFIGURATION
# -----------------------------

RAW_DATA_PATH = "data/raw"

MYSQL_USER = "root"
MYSQL_PASSWORD = "Sinchana@21"
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DATABASE = "olist_kpi_engine"


connection_url = URL.create(
    drivername="mysql+pymysql",
    username=MYSQL_USER,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST,
    port=int(MYSQL_PORT),
    database=MYSQL_DATABASE,
)

engine = create_engine(connection_url)

TABLES = {
    "olist_customers_dataset.csv": "customers",
    "olist_geolocation_dataset.csv": "geolocation",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "payments",
    "olist_order_reviews_dataset.csv": "reviews",
    "olist_orders_dataset.csv": "orders",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "product_category_name_translation.csv": "category_translation"
}

# -----------------------------
# 2. LOAD CSV FILES INTO MYSQL
# -----------------------------

for file_name, table_name in TABLES.items():
    file_path = os.path.join(RAW_DATA_PATH, file_name)

    if not os.path.exists(file_path):
        print(f"Missing file: {file_name}")
        continue

    print(f"Loading {file_name} into MySQL table: {table_name}")

    df = pd.read_csv(file_path)

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",
        index=False,
        chunksize=5000
    )

    print(f"Loaded {len(df):,} rows into {table_name}")

print("All files loaded into MySQL successfully.")