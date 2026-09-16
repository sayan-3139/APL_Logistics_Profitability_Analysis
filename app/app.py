import streamlit as st
import pandas as pd
import os

# Page configuration
st.set_page_config(
    page_title="APL Logistics Profitability Analysis",
    page_icon="📊",
    layout="wide"
)

# Load dataset
DATA_PATH = os.path.join("data", "APL_Logistics.csv")

df = pd.read_csv(DATA_PATH, encoding="cp1252")

# Title
st.title("📊 APL Logistics Profitability Analysis")
st.markdown(
    "Interactive dashboard for analyzing sales, profitability, "
    "customers, markets, products and shipping performance."
)

st.divider()

# KPI calculations
total_sales = df["Sales"].sum()
total_profit = df["Order Profit Per Order"].sum()
avg_profit = df["Order Profit Per Order"].mean()
total_orders = len(df)

# KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Average Order Profit", f"${avg_profit:,.2f}")
col4.metric("Total Orders", f"{total_orders:,}")

st.divider()

# Sidebar filters
st.sidebar.header("🔎 Filters")

markets = st.sidebar.multiselect(
    "Select Market",
    options=sorted(df["Market"].unique()),
    default=sorted(df["Market"].unique())
)

segments = st.sidebar.multiselect(
    "Select Customer Segment",
    options=sorted(df["Customer Segment"].unique()),
    default=sorted(df["Customer Segment"].unique())
)

shipping_modes = st.sidebar.multiselect(
    "Select Shipping Mode",
    options=sorted(df["Shipping Mode"].unique()),
    default=sorted(df["Shipping Mode"].unique())
)

# Apply filters
filtered_df = df[
    (df["Market"].isin(markets)) &
    (df["Customer Segment"].isin(segments)) &
    (df["Shipping Mode"].isin(shipping_modes))
]

# Filtered KPIs
st.subheader("📈 Filtered Performance")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Filtered Sales",
    f"${filtered_df['Sales'].sum():,.2f}"
)

c2.metric(
    "Filtered Profit",
    f"${filtered_df['Order Profit Per Order'].sum():,.2f}"
)

c3.metric(
    "Average Profit",
    f"${filtered_df['Order Profit Per Order'].mean():,.2f}"
)

c4.metric(
    "Orders",
    f"{len(filtered_df):,}"
)

st.divider()

# Profit by Market
st.subheader("🌍 Profit by Market")

market_profit = (
    filtered_df.groupby("Market")["Order Profit Per Order"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(market_profit)

# Profit by Customer Segment
st.subheader("👥 Profit by Customer Segment")

segment_profit = (
    filtered_df.groupby("Customer Segment")["Order Profit Per Order"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(segment_profit)

# Profit by Shipping Mode
st.subheader("🚚 Profit by Shipping Mode")

shipping_profit = (
    filtered_df.groupby("Shipping Mode")["Order Profit Per Order"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(shipping_profit)

st.divider()

# Product profitability
st.subheader("🏆 Top 10 Most Profitable Products")

product_profit = (
    filtered_df.groupby("Product Name")
    .agg(
        Orders=("Product Name", "size"),
        Sales=("Sales", "sum"),
        Profit=("Order Profit Per Order", "sum")
    )
    .sort_values("Profit", ascending=False)
    .head(10)
)

st.dataframe(
    product_profit,
    use_container_width=True
)

# Least profitable products
st.subheader("⚠️ Bottom 10 Least Profitable Products")

bottom_products = (
    filtered_df.groupby("Product Name")
    .agg(
        Orders=("Product Name", "size"),
        Sales=("Sales", "sum"),
        Profit=("Order Profit Per Order", "sum")
    )
    .sort_values("Profit", ascending=True)
    .head(10)
)

st.dataframe(
    bottom_products,
    use_container_width=True
)

st.divider()

# Delivery analysis
st.subheader("📦 Delivery Status")

delivery_status = (
    filtered_df["Delivery Status"]
    .value_counts()
)

st.bar_chart(delivery_status)

# Dataset preview
with st.expander("📋 View Dataset"):
    st.dataframe(
        filtered_df.head(100),
        use_container_width=True
    )

st.caption(
    "APL Logistics Profitability Analysis | "
    "Built with Python, Pandas and Streamlit"
)