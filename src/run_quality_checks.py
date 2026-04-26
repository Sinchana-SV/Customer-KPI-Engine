import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# -----------------------------
# 1. Load database credentials
# -----------------------------

load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT"))
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

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
# 2. Define quality checks
# -----------------------------

QUALITY_CHECKS = [
    {
        "check_name": "Duplicate order_id in orders",
        "query": """
            SELECT COUNT(*) AS issue_count
            FROM (
                SELECT order_id
                FROM orders
                GROUP BY order_id
                HAVING COUNT(*) > 1
            ) t;
        """
    },
    {
        "check_name": "Missing customer_id in orders",
        "query": """
            SELECT COUNT(*) AS issue_count
            FROM orders
            WHERE customer_id IS NULL;
        """
    },
    {
        "check_name": "Orders without payment record",
        "query": """
            SELECT COUNT(*) AS issue_count
            FROM orders o
            LEFT JOIN payments p
                ON o.order_id = p.order_id
            WHERE p.order_id IS NULL;
        """
    },
    {
        "check_name": "Orders without customer record",
        "query": """
            SELECT COUNT(*) AS issue_count
            FROM orders o
            LEFT JOIN customers c
                ON o.customer_id = c.customer_id
            WHERE c.customer_id IS NULL;
        """
    },
    {
        "check_name": "Negative payment values",
        "query": """
            SELECT COUNT(*) AS issue_count
            FROM payments
            WHERE payment_value < 0;
        """
    },
    {
        "check_name": "Order items without product_id",
        "query": """
            SELECT COUNT(*) AS issue_count
            FROM order_items
            WHERE product_id IS NULL;
        """
    },
    {
        "check_name": "Delivered date before purchase date",
        "query": """
            SELECT COUNT(*) AS issue_count
            FROM orders
            WHERE order_delivered_customer_date < order_purchase_timestamp;
        """
    },
    {
        "check_name": "Missing review scores",
        "query": """
            SELECT COUNT(*) AS issue_count
            FROM reviews
            WHERE review_score IS NULL;
        """
    },
    {
        "check_name": "Negative item prices",
        "query": """
            SELECT COUNT(*) AS issue_count
            FROM order_items
            WHERE price < 0;
        """
    },
    {
        "check_name": "Negative freight values",
        "query": """
            SELECT COUNT(*) AS issue_count
            FROM order_items
            WHERE freight_value < 0;
        """
    }
]

# -----------------------------
# 3. Run checks
# -----------------------------

def run_quality_checks():
    results = []

    with engine.connect() as conn:
        for check in QUALITY_CHECKS:
            result = conn.execute(text(check["query"]))
            issue_count = result.fetchone()[0]

            if issue_count == 0:
                status = "PASS"
            else:
                status = "FAIL"

            results.append({
                "check_name": check["check_name"],
                "issue_count": issue_count,
                "status": status
            })

    report = pd.DataFrame(results)

    os.makedirs("outputs/reports", exist_ok=True)

    output_path = "outputs/reports/data_quality_report.csv"
    report.to_csv(output_path, index=False)

    print("\nDATA QUALITY REPORT")
    print(report)

    print(f"\nSaved quality report to: {output_path}")

    failed_checks = report[report["status"] == "FAIL"]

    if len(failed_checks) > 0:
        print("\nSome checks failed. This does not mean the project failed.")
        print("It means we found real data issues and documented them.")
    else:
        print("\nAll checks passed.")

if __name__ == "__main__":
    run_quality_checks()