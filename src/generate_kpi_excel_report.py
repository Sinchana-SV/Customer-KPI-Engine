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
# 3. Output path
# -----------------------------

OUTPUT_FOLDER = "outputs/reports"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

EXCEL_OUTPUT_PATH = os.path.join(
    OUTPUT_FOLDER,
    "customer_kpi_engine_report.xlsx"
)

# -----------------------------
# 4. KPI queries
# -----------------------------

KPI_QUERIES = {
    "Monthly_GMV": "SELECT * FROM kpi_monthly_gmv",
    "Repeat_Customers": "SELECT * FROM kpi_repeat_customer_rate",
    "Delivery_By_State": "SELECT * FROM kpi_delivery_by_state",
    "Review_Trend": "SELECT * FROM kpi_review_trend",
    "Revenue_Concentration": "SELECT * FROM kpi_revenue_concentration",
    "Top_10_Sellers": "SELECT * FROM kpi_top_10_sellers"
}

# -----------------------------
# 5. Generate Excel report
# -----------------------------

def generate_excel_report():
    print("Generating Excel KPI report...\n")

    with pd.ExcelWriter(EXCEL_OUTPUT_PATH, engine="openpyxl") as writer:
        for sheet_name, query in KPI_QUERIES.items():
            print(f"Writing sheet: {sheet_name}")

            df = pd.read_sql(query, engine)

            df.to_excel(
                writer,
                sheet_name=sheet_name,
                index=False
            )

    print("\nExcel report generated successfully.")
    print(f"Saved at: {EXCEL_OUTPUT_PATH}")

if __name__ == "__main__":
    generate_excel_report()