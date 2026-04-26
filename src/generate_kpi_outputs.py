import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# -----------------------------
# 1. Load environment variables
# -----------------------------

load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT"))
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

# -----------------------------
# 2. Create database connection
# -----------------------------

connection_url = URL.create(
    drivername="mysql+pymysql",
    username=MYSQL_USER,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    database=MYSQL_DATABASE,
)

engine = create_engine(connection_url)

# -----------------------------
# 3. Output folder
# -----------------------------

OUTPUT_PATH = "data/exports"
os.makedirs(OUTPUT_PATH, exist_ok=True)

# -----------------------------
# 4. Define KPI queries
# -----------------------------

KPI_QUERIES = {
    "monthly_gmv": "SELECT * FROM kpi_monthly_gmv",
    "repeat_customer_rate": "SELECT * FROM kpi_repeat_customer_rate",
    "delivery_by_state": "SELECT * FROM kpi_delivery_by_state",
    "review_trend": "SELECT * FROM kpi_review_trend",
    "revenue_concentration": "SELECT * FROM kpi_revenue_concentration",
    "top_10_sellers": "SELECT * FROM kpi_top_10_sellers"
}

# -----------------------------
# 5. Run queries and export
# -----------------------------

def generate_reports():
    print("Generating KPI reports...\n")

    for name, query in KPI_QUERIES.items():
        print(f"Processing: {name}")

        df = pd.read_sql(query, engine)

        file_path = os.path.join(OUTPUT_PATH, f"{name}.csv")
        df.to_csv(file_path, index=False)

        print(f"Saved: {file_path}")

    print("\nAll KPI reports generated successfully.")

if __name__ == "__main__":
    generate_reports()