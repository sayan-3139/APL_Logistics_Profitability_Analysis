import pandas as pd
import matplotlib.pyplot as plt
import os

# ============================================================
# APL LOGISTICS - PROFITABILITY VISUALIZATIONS
# ============================================================

# Load dataset
df = pd.read_csv(
    "data/APL_Logistics.csv",
    encoding="cp1252"
)

# Create images folder if it doesn't exist
os.makedirs("images", exist_ok=True)

print("=" * 60)
print("APL LOGISTICS - VISUALIZATION ANALYSIS")
print("=" * 60)


# ============================================================
# 1. PROFIT BY MARKET
# ============================================================

market_profit = (
    df.groupby("Market")["Order Profit Per Order"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))
market_profit.plot(kind="bar")
plt.title("Total Profit by Market")
plt.xlabel("Market")
plt.ylabel("Total Profit")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("images/profit_by_market.png", dpi=300)
plt.show()
plt.close()

print("1. Profit by Market chart created.")


# ============================================================
# 2. PROFIT BY CUSTOMER SEGMENT
# ============================================================

segment_profit = (
    df.groupby("Customer Segment")["Order Profit Per Order"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(8, 5))
segment_profit.plot(kind="bar")
plt.title("Total Profit by Customer Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Total Profit")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("images/profit_by_customer_segment.png", dpi=300)
plt.show()
plt.close()

print("2. Customer Segment chart created.")


# ============================================================
# 3. PROFIT BY SHIPPING MODE
# ============================================================

shipping_profit = (
    df.groupby("Shipping Mode")["Order Profit Per Order"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(9, 5))
shipping_profit.plot(kind="bar")
plt.title("Total Profit by Shipping Mode")
plt.xlabel("Shipping Mode")
plt.ylabel("Total Profit")
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig("images/profit_by_shipping_mode.png", dpi=300)
plt.show()
plt.close()

print("3. Shipping Mode chart created.")


# ============================================================
# 4. TOP 10 MOST PROFITABLE PRODUCTS
# ============================================================

product_profit = (
    df.groupby("Product Name")["Order Profit Per Order"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 7))
product_profit.plot(kind="barh")
plt.title("Top 10 Most Profitable Products")
plt.xlabel("Total Profit")
plt.ylabel("Product")
plt.tight_layout()

plt.savefig("images/top_10_profitable_products.png", dpi=300)
plt.show()
plt.close()

print("4. Top 10 products chart created.")


# ============================================================
# 5. BOTTOM 10 LEAST PROFITABLE PRODUCTS
# ============================================================

least_profit = (
    df.groupby("Product Name")["Order Profit Per Order"]
    .sum()
    .sort_values(ascending=True)
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 7))
least_profit.plot(kind="barh")
plt.title("Bottom 10 Least Profitable Products")
plt.xlabel("Total Profit")
plt.ylabel("Product")
plt.tight_layout()

plt.savefig("images/bottom_10_profitable_products.png", dpi=300)
plt.show()
plt.close()

print("5. Bottom 10 products chart created.")


# ============================================================
# FINISHED
# ============================================================

print("\n" + "=" * 60)
print("ALL VISUALIZATIONS CREATED SUCCESSFULLY")
print("=" * 60)

print("\nCharts saved in:")
print("images/")