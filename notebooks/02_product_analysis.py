import pandas as pd

# Load dataset
df = pd.read_csv(
    "data/APL_Logistics.csv",
    encoding="cp1252"
)

print("=" * 60)
print("APL LOGISTICS - PRODUCT PROFITABILITY ANALYSIS")
print("=" * 60)

# Overall product performance
product_analysis = (
    df.groupby("Product Name")
    .agg(
        Orders=("Product Name", "count"),
        Sales=("Sales", "sum"),
        Profit=("Order Profit Per Order", "sum"),
        Avg_Profit=("Order Profit Per Order", "mean")
    )
    .sort_values("Profit", ascending=False)
)

print("\nTOP 10 MOST PROFITABLE PRODUCTS")
print(product_analysis.head(10).round(2))

print("\nBOTTOM 10 LEAST PROFITABLE PRODUCTS")
print(product_analysis.tail(10).round(2))

# Product category performance
category_analysis = (
    df.groupby("Category Name")
    .agg(
        Orders=("Category Name", "count"),
        Sales=("Sales", "sum"),
        Profit=("Order Profit Per Order", "sum"),
        Avg_Profit=("Order Profit Per Order", "mean")
    )
    .sort_values("Profit", ascending=False)
)

print("\n" + "=" * 60)
print("PROFIT BY CATEGORY")
print("=" * 60)

print(category_analysis.round(2))