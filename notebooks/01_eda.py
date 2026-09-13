import pandas as pd

# Load dataset
df = pd.read_csv("data/APL_Logistics.csv", encoding="cp1252")

print("=" * 60)
print("APL LOGISTICS PROFITABILITY ANALYSIS")
print("=" * 60)

# Basic information
print("\nDataset Shape:")
print(df.shape)

# Overall profitability
print("\nOverall Business Performance:")
print("Total Sales:", round(df["Sales"].sum(), 2))
print("Total Order Profit:", round(df["Order Profit Per Order"].sum(), 2))
print("Average Order Profit:", round(df["Order Profit Per Order"].mean(), 2))

# Profit by Market
print("\n" + "=" * 60)
print("PROFIT BY MARKET")
print("=" * 60)

market_profit = (
    df.groupby("Market")
    .agg(
        Orders=("Order Profit Per Order", "count"),
        Sales=("Sales", "sum"),
        Profit=("Order Profit Per Order", "sum"),
        Avg_Profit=("Order Profit Per Order", "mean")
    )
    .sort_values("Profit", ascending=False)
)

print(market_profit.round(2))

# Profit by Customer Segment
print("\n" + "=" * 60)
print("PROFIT BY CUSTOMER SEGMENT")
print("=" * 60)

segment_profit = (
    df.groupby("Customer Segment")
    .agg(
        Orders=("Order Profit Per Order", "count"),
        Sales=("Sales", "sum"),
        Profit=("Order Profit Per Order", "sum"),
        Avg_Profit=("Order Profit Per Order", "mean")
    )
    .sort_values("Profit", ascending=False)
)

print(segment_profit.round(2))

# Profit by Shipping Mode
print("\n" + "=" * 60)
print("PROFIT BY SHIPPING MODE")
print("=" * 60)

shipping_profit = (
    df.groupby("Shipping Mode")
    .agg(
        Orders=("Order Profit Per Order", "count"),
        Sales=("Sales", "sum"),
        Profit=("Order Profit Per Order", "sum"),
        Avg_Profit=("Order Profit Per Order", "mean")
    )
    .sort_values("Profit", ascending=False)
)

print(shipping_profit.round(2))