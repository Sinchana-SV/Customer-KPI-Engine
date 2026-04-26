import os
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# 1. Paths
# -----------------------------

EXCEL_PATH = "outputs/reports/customer_kpi_engine_report.xlsx"
CHARTS_PATH = "outputs/charts"

os.makedirs(CHARTS_PATH, exist_ok=True)

# -----------------------------
# 2. Load Excel Sheets
# -----------------------------

excel_file = pd.ExcelFile(EXCEL_PATH)

monthly_gmv = excel_file.parse("Monthly_GMV")
delivery = excel_file.parse("Delivery_By_State")
reviews = excel_file.parse("Review_Trend")
top_sellers = excel_file.parse("Top_10_Sellers")

# -----------------------------
# 3. Monthly GMV Trend
# -----------------------------

plt.figure()
plt.plot(monthly_gmv["order_month"], monthly_gmv["monthly_gmv"], marker="o")
plt.xticks(rotation=45)
plt.title("Monthly GMV Trend")
plt.xlabel("Month")
plt.ylabel("GMV")
plt.tight_layout()

plt.savefig(f"{CHARTS_PATH}/monthly_gmv.png")
plt.close()

# -----------------------------
# 4. Order Volume Trend
# -----------------------------

plt.figure()
plt.plot(monthly_gmv["order_month"], monthly_gmv["total_orders"], marker="o")
plt.xticks(rotation=45)
plt.title("Monthly Order Volume")
plt.xlabel("Month")
plt.ylabel("Orders")
plt.tight_layout()

plt.savefig(f"{CHARTS_PATH}/order_volume.png")
plt.close()

# -----------------------------
# 5. Review Sentiment Trend
# -----------------------------

plt.figure()
plt.plot(reviews["order_month"], reviews["positive_review_pct"], label="Positive")
plt.plot(reviews["order_month"], reviews["negative_review_pct"], label="Negative")
plt.xticks(rotation=45)
plt.title("Review Sentiment Trend")
plt.xlabel("Month")
plt.ylabel("Percentage")
plt.legend()
plt.tight_layout()

plt.savefig(f"{CHARTS_PATH}/review_trend.png")
plt.close()

# -----------------------------
# 6. Delivery Performance (Top 10 states)
# -----------------------------

top_delivery = delivery.sort_values("avg_delivery_days", ascending=False).head(10)

plt.figure()
plt.bar(top_delivery["customer_state"], top_delivery["avg_delivery_days"])
plt.title("Top 10 States by Delivery Time")
plt.xlabel("State")
plt.ylabel("Days")
plt.tight_layout()

plt.savefig(f"{CHARTS_PATH}/delivery_by_state.png")
plt.close()

# -----------------------------
# 7. Top Sellers Revenue
# -----------------------------

plt.figure()
plt.bar(top_sellers["seller_id"], top_sellers["seller_gmv"])
plt.xticks(rotation=90)
plt.title("Top 10 Sellers by Revenue")
plt.xlabel("Seller")
plt.ylabel("GMV")
plt.tight_layout()

plt.savefig(f"{CHARTS_PATH}/top_sellers.png")
plt.close()

print("Charts created successfully in outputs/charts/")