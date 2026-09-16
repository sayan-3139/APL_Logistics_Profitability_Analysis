import streamlit as st
import pandas as pd
import os

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="APL Logistics Profitability Analysis",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# LOAD DATASET
# ============================================================

DATA_PATH = os.path.join("data", "APL_Logistics.csv")

try:
    df = pd.read_csv(DATA_PATH, encoding="cp1252")
except FileNotFoundError:
    st.error(f"Dataset not found: {DATA_PATH}")
    st.stop()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()


# ============================================================
# BASIC DATA CLEANING
# ============================================================

df.columns = df.columns.str.strip()

# Numeric columns
numeric_columns = [
    "Sales",
    "Order Profit Per Order",
    "Discount"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# Remove rows where important financial values are missing
if "Sales" in df.columns and "Order Profit Per Order" in df.columns:
    df = df.dropna(
        subset=["Sales", "Order Profit Per Order"]
    ).copy()


# ============================================================
# TITLE
# ============================================================

st.title("📊 APL Logistics Profitability Analysis")

st.markdown(
    """
    **Interactive business analytics dashboard** for analyzing
    sales, profitability, customers, products, markets,
    discounts, shipping and delivery performance.
    """
)

st.divider()


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔎 Dashboard Filters")


def get_options(column):
    """Return sorted unique values for an existing column."""
    if column in df.columns:
        return sorted(df[column].dropna().unique().tolist())
    return []


# Market
markets = get_options("Market")

if markets:
    selected_markets = st.sidebar.multiselect(
        "🌍 Market",
        options=markets,
        default=markets
    )
else:
    selected_markets = []


# Customer Segment
segments = get_options("Customer Segment")

if segments:
    selected_segments = st.sidebar.multiselect(
        "👥 Customer Segment",
        options=segments,
        default=segments
    )
else:
    selected_segments = []


# Category
categories = get_options("Category")

if categories:
    selected_categories = st.sidebar.multiselect(
        "📦 Category",
        options=categories,
        default=categories
    )
else:
    selected_categories = []

    # Product
products = get_options("Product Name")

if products:
    selected_products = st.sidebar.multiselect(
        "🏷️ Product",
        options=products,
        default=products
    )
else:
    selected_products = []


# Shipping Mode
shipping_modes = get_options("Shipping Mode")

if shipping_modes:
    selected_shipping = st.sidebar.multiselect(
        "🚚 Shipping Mode",
        options=shipping_modes,
        default=shipping_modes
    )
else:
    selected_shipping = []


# Order Region
regions = get_options("Order Region")

if regions:
    selected_regions = st.sidebar.multiselect(
        "📍 Order Region",
        options=regions,
        default=regions
    )
else:
    selected_regions = []


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()

if "Market" in df.columns and selected_markets:
    filtered_df = filtered_df[
        filtered_df["Market"].isin(selected_markets)
    ]

if "Customer Segment" in df.columns and selected_segments:
    filtered_df = filtered_df[
        filtered_df["Customer Segment"].isin(selected_segments)
    ]

if "Category" in df.columns and selected_categories:
    filtered_df = filtered_df[
        filtered_df["Category"].isin(selected_categories)
    ]

if "Product Name" in df.columns and selected_products:
    filtered_df = filtered_df[
        filtered_df["Product Name"].isin(selected_products)
    ]

if "Shipping Mode" in df.columns and selected_shipping:
    filtered_df = filtered_df[
        filtered_df["Shipping Mode"].isin(selected_shipping)
    ]

if "Order Region" in df.columns and selected_regions:
    filtered_df = filtered_df[
        filtered_df["Order Region"].isin(selected_regions)
    ]


# ============================================================
# EMPTY DATA CHECK
# ============================================================

if filtered_df.empty:
    st.warning(
        "⚠️ No records match the selected filters. "
        "Please change your filters."
    )
    st.stop()


# ============================================================
# FINANCIAL CALCULATIONS
# ============================================================

total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df[
    "Order Profit Per Order"
].sum()

total_orders = len(filtered_df)

avg_profit = filtered_df[
    "Order Profit Per Order"
].mean()

if total_sales != 0:
    profit_margin = (total_profit / total_sales) * 100
else:
    profit_margin = 0


# ============================================================
# EXECUTIVE KPI SECTION
# ============================================================

st.subheader("📌 Executive Overview")

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric(
    "💰 Total Sales",
    f"${total_sales:,.2f}"
)

k2.metric(
    "📈 Total Profit",
    f"${total_profit:,.2f}"
)

k3.metric(
    "📊 Profit Margin",
    f"{profit_margin:.2f}%"
)

k4.metric(
    "🧾 Total Orders",
    f"{total_orders:,}"
)

k5.metric(
    "💵 Avg. Order Profit",
    f"${avg_profit:,.2f}"
)


st.divider()


# ============================================================
# OVERVIEW TAB
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📊 Overview",
        "👥 Customer Analysis",
        "📦 Product Analysis",
        "🏷️ Discount Analysis",
        "🌍 Market & Shipping"
    ]
)


# ============================================================
# TAB 1 - OVERVIEW
# ============================================================

with tab1:

    st.subheader("📈 Sales & Profit Overview")

    overview_col1, overview_col2 = st.columns(2)

    # Sales by Market
    with overview_col1:

        if "Market" in filtered_df.columns:

            market_sales = (
                filtered_df
                .groupby("Market")["Sales"]
                .sum()
                .sort_values(ascending=False)
            )

            st.markdown("### 💰 Sales by Market")
            st.bar_chart(market_sales)

    # Profit by Market
    with overview_col2:

        if "Market" in filtered_df.columns:

            market_profit = (
                filtered_df
                .groupby("Market")[
                    "Order Profit Per Order"
                ]
                .sum()
                .sort_values(ascending=False)
            )

            st.markdown("### 📈 Profit by Market")
            st.bar_chart(market_profit)


    st.divider()

    # Segment analysis
    if "Customer Segment" in filtered_df.columns:

        st.subheader("👥 Profit by Customer Segment")

        segment_profit = (
            filtered_df
            .groupby("Customer Segment")[
                "Order Profit Per Order"
            ]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(segment_profit)


    # Delivery status
    if "Delivery Status" in filtered_df.columns:

        st.divider()

        st.subheader("📦 Delivery Status")

        delivery_status = (
            filtered_df["Delivery Status"]
            .value_counts()
        )

        st.bar_chart(delivery_status)


# ============================================================
# TAB 2 - CUSTOMER ANALYSIS
# ============================================================

with tab2:

    st.subheader("👥 Customer Value Analysis")

    # Customer ID column detection
    customer_column = None

    possible_customer_columns = [
        "Customer Id",
        "Customer ID",
        "Customer Id ",
        "Customer"
    ]

    for col in possible_customer_columns:
        if col in filtered_df.columns:
            customer_column = col
            break


    if customer_column:

        customer_analysis = (
            filtered_df
            .groupby(customer_column)
            .agg(
                Orders=("Sales", "size"),
                Sales=("Sales", "sum"),
                Profit=(
                    "Order Profit Per Order",
                    "sum"
                )
            )
        )

        customer_analysis["Profit Margin %"] = (
            customer_analysis["Profit"]
            / customer_analysis["Sales"]
            .replace(0, pd.NA)
            * 100
        )

        customer_analysis = (
            customer_analysis
            .sort_values("Profit", ascending=False)
        )


        # ----------------------------------------------------
        # Customer Value Index
        # ----------------------------------------------------

        def normalize(series):

            minimum = series.min()
            maximum = series.max()

            if maximum == minimum:
                return pd.Series(
                    [50] * len(series),
                    index=series.index
                )

            return (
                (series - minimum)
                / (maximum - minimum)
                * 100
            )


        customer_analysis["Sales Score"] = normalize(
            customer_analysis["Sales"]
        )

        customer_analysis["Profit Score"] = normalize(
            customer_analysis["Profit"]
        )

        customer_analysis["Order Score"] = normalize(
            customer_analysis["Orders"]
        )

        customer_analysis["Customer Value Index"] = (
            customer_analysis["Sales Score"] * 0.30
            + customer_analysis["Profit Score"] * 0.50
            + customer_analysis["Order Score"] * 0.20
        )


        st.markdown(
            """
            **Customer Value Index (CVI)** combines customer
            sales, profitability and order frequency into a
            normalized 0–100 analytical score.
            """
        )


        c1, c2 = st.columns(2)

        with c1:

            st.markdown("### 🏆 Top Customers")

            st.dataframe(
                customer_analysis[
                    [
                        "Orders",
                        "Sales",
                        "Profit",
                        "Profit Margin %",
                        "Customer Value Index"
                    ]
                ].head(10),
                use_container_width=True
            )


        with c2:

            st.markdown("### 📊 Customer Value Index")

            cvi_chart = (
                customer_analysis[
                    "Customer Value Index"
                ]
                .head(10)
            )

            st.bar_chart(cvi_chart)


    else:

        st.info(
            "Customer ID column was not found in the dataset."
        )


    # Segment profitability
    if "Customer Segment" in filtered_df.columns:

        st.divider()

        st.subheader("Customer Segment Performance")

        segment_table = (
            filtered_df
            .groupby("Customer Segment")
            .agg(
                Orders=("Sales", "size"),
                Sales=("Sales", "sum"),
                Profit=(
                    "Order Profit Per Order",
                    "sum"
                )
            )
        )

        segment_table["Profit Margin %"] = (
            segment_table["Profit"]
            / segment_table["Sales"]
            .replace(0, pd.NA)
            * 100
        )

# Customer Segment percentage contribution
total_segment_sales = segment_table["Sales"].sum()

segment_table["Sales Contribution %"] = (
    segment_table["Sales"]
    / total_segment_sales
    * 100
)

segment_display = segment_table.copy()

segment_display["Sales"] = segment_display["Sales"].map(
    lambda x: f"${x:,.2f}"
)

segment_display["Profit"] = segment_display["Profit"].map(
    lambda x: f"${x:,.2f}"
)

segment_display["Profit Margin %"] = segment_display["Profit Margin %"].map(
    lambda x: f"{x:.2f}%"
)

# Make Customer Segment a visible column
segment_table = segment_table.reset_index()

st.dataframe(
    segment_table.style.format({
        "Sales": "${:,.2f}",
        "Profit": "${:,.2f}",
        "Profit Margin %": "{:.2f}%",
        "Sales Contribution %": "{:.2f}%"
    }),
    use_container_width=True,
    hide_index=True
)
# ============================================================
# TAB 3 - PRODUCT ANALYSIS
# ============================================================

with tab3:

    st.subheader("📦 Product & Category Profitability")


    # --------------------------------------------------------
    # Product analysis
    # --------------------------------------------------------

    if "Product Name" in filtered_df.columns:

        product_analysis = (
            filtered_df
            .groupby("Product Name")
            .agg(
                Orders=("Product Name", "size"),
                Sales=("Sales", "sum"),
                Profit=(
                    "Order Profit Per Order",
                    "sum"
                )
            )
        )

        product_analysis["Profit Margin %"] = (
            product_analysis["Profit"]
            / product_analysis["Sales"]
            .replace(0, pd.NA)
            * 100
        )


        col1, col2 = st.columns(2)


        with col1:

            st.markdown(
                "### 🏆 Top 10 Profitable Products"
            )

            top_products = (
                product_analysis
                .sort_values(
                    "Profit",
                    ascending=False
                )
                .head(10)
            )

            st.dataframe(
                top_products,
                use_container_width=True
            )


        with col2:

            st.markdown(
                "### ⚠️ Bottom 10 Products"
            )

            bottom_products = (
                product_analysis
                .sort_values(
                    "Profit",
                    ascending=True
                )
                .head(10)
            )

            st.dataframe(
                bottom_products,
                use_container_width=True
            )


    # --------------------------------------------------------
    # Category analysis
    # --------------------------------------------------------

    if "Category" in filtered_df.columns:

        st.divider()

        st.subheader("📊 Category Profitability")

        category_analysis = (
            filtered_df
            .groupby("Category")
            .agg(
                Orders=("Sales", "size"),
                Sales=("Sales", "sum"),
                Profit=(
                    "Order Profit Per Order",
                    "sum"
                )
            )
        )

        category_analysis["Profit Margin %"] = (
            category_analysis["Profit"]
            / category_analysis["Sales"]
            .replace(0, pd.NA)
            * 100
        )

        st.dataframe(
            category_analysis.sort_values(
                "Profit",
                ascending=False
            ),
            use_container_width=True
        )

        st.markdown("### 💰 Category Profit")

        st.bar_chart(
            category_analysis["Profit"]
            .sort_values(ascending=False)
        )

# =========================================================
# LOSS-MAKING CATEGORIES
# =========================================================

st.subheader("🚨 Loss-Making Categories")

# Create a fresh category analysis directly from filtered_df
loss_category_analysis = (
    filtered_df
    .groupby("Category Name")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Order Profit Per Order", "sum"),
        Orders=("Order Profit Per Order", "size")
    )
    .reset_index()
)

# Calculate profit margin
loss_category_analysis["Profit Margin %"] = (
    loss_category_analysis["Profit"]
    / loss_category_analysis["Sales"].replace(0, pd.NA)
    * 100
)

# Keep only categories with negative total profit
loss_categories = loss_category_analysis[
    loss_category_analysis["Profit"] < 0
].sort_values(
    "Profit",
    ascending=True
)

if loss_categories.empty:
    st.success(
        "✅ No loss-making categories found for the current filters."
    )
else:
    st.dataframe(
        loss_categories[
            [
                "Category Name",
                "Sales",
                "Profit",
                "Orders",
                "Profit Margin %"
            ]
        ],
        use_container_width=True
    )

    st.caption(
        "Loss-making categories are categories where total "
        "profit is below zero."
    )

# =========================================================
# CATEGORY PROFITABILITY HEATMAP
# =========================================================

st.subheader("🔥 Category Profitability Heatmap")

# Create category-level analysis from the filtered dataset
category_analysis = (
    filtered_df
    .groupby("Category Name")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Order Profit Per Order", "sum"),
        Orders=("Order Profit Per Order", "size")
    )
    .reset_index()
)

# Calculate Profit Margin
category_analysis["Profit Margin %"] = (
    category_analysis["Profit"]
    / category_analysis["Sales"].replace(0, pd.NA)
    * 100
)

# Sort by profit
category_analysis = category_analysis.sort_values(
    "Profit",
    ascending=False
)

# Display heatmap-style table
if category_analysis.empty:

    st.info("No category data available for the selected filters.")

else:

    st.dataframe(
        category_analysis.style.background_gradient(
            subset=["Sales", "Profit", "Profit Margin %"]
        ),
        use_container_width=True
    )

    st.caption(
        "The heatmap highlights relative Sales, Profit and "
        "Profit Margin performance across product categories."
    )


# =========================================================
# LOSS-MAKING CATEGORIES
# =========================================================

st.subheader("🚨 Loss-Making Categories")

# Select categories where total profit is negative
loss_categories = category_analysis[
    category_analysis["Profit"] < 0
].copy()

if loss_categories.empty:

    st.success(
        "✅ No loss-making categories found for the current filters."
    )

else:

    loss_categories = loss_categories.sort_values(
        "Profit",
        ascending=True
    )

    st.dataframe(
        loss_categories[
            [
                "Category Name",
                "Sales",
                "Profit",
                "Orders",
                "Profit Margin %"
            ]
        ],
        use_container_width=True
    )

    st.caption(
        "Loss-making categories are categories where total "
        "profit is below zero."
    )


# ============================================================
# DISCOUNT ANALYSIS
# ============================================================

with tab4:
    st.subheader("🏷️ Discount Impact Analyzer")

    # Actual columns available in APL Logistics dataset
    discount_rate_col = "Order Item Discount Rate"
    discount_amount_col = "Order Item Discount"
    profit_ratio_col = "Order Item Profit Ratio"
    profit_col = "Order Profit Per Order"
    sales_col = "Sales"

    # Check required columns
    required_discount_cols = [
        discount_rate_col,
        discount_amount_col,
        profit_ratio_col,
        profit_col,
        sales_col
    ]

    missing_cols = [
        col for col in required_discount_cols
        if col not in filtered_df.columns
    ]

    if missing_cols:
        st.error(
            "Required discount columns are missing: "
            + ", ".join(missing_cols)
        )

    elif filtered_df.empty:
        st.warning("No data available for the selected filters.")

    else:
        # ----------------------------------------------------
        # Prepare discount data
        # ----------------------------------------------------

        discount_df = filtered_df.copy()

        discount_df[discount_rate_col] = pd.to_numeric(
            discount_df[discount_rate_col],
            errors="coerce"
        )

        discount_df[discount_amount_col] = pd.to_numeric(
            discount_df[discount_amount_col],
            errors="coerce"
        )

        discount_df[profit_ratio_col] = pd.to_numeric(
            discount_df[profit_ratio_col],
            errors="coerce"
        )

        discount_df[profit_col] = pd.to_numeric(
            discount_df[profit_col],
            errors="coerce"
        )

        discount_df[sales_col] = pd.to_numeric(
            discount_df[sales_col],
            errors="coerce"
        )

        discount_df = discount_df.dropna(
            subset=[
                discount_rate_col,
                discount_amount_col,
                profit_ratio_col,
                profit_col,
                sales_col
            ]
        )

        # Convert discount rate to percentage
        discount_df["Discount %"] = (
            discount_df[discount_rate_col] * 100
        )

        # Profit margin based on Sales
        discount_df["Profit Margin %"] = (
            discount_df[profit_col]
            / discount_df[sales_col].replace(0, pd.NA)
        ) * 100

        # ----------------------------------------------------
        # KPI CARDS
        # ----------------------------------------------------

        avg_discount = discount_df[discount_rate_col].mean() * 100

        total_discount = discount_df[discount_amount_col].sum()

        avg_profit_ratio = (
            discount_df[profit_ratio_col].mean() * 100
        )

        total_discounted_orders = (
            discount_df[discount_rate_col].gt(0).sum()
        )

        k1, k2, k3, k4 = st.columns(4)

        k1.metric(
            "Average Discount",
            f"{avg_discount:.2f}%"
        )

        k2.metric(
            "Total Discount Amount",
            f"${total_discount:,.2f}"
        )

        k3.metric(
            "Avg. Profit Ratio",
            f"{avg_profit_ratio:.2f}%"
        )

        k4.metric(
            "Discounted Orders",
            f"{total_discounted_orders:,}"
        )

        st.divider()

        # ----------------------------------------------------
        # DISCOUNT RATE vs PROFIT MARGIN
        # ----------------------------------------------------

        st.subheader("📉 Discount Rate vs Profit Margin")

        discount_impact = (
            discount_df
            .groupby("Discount %")
            .agg(
                Orders=(profit_col, "size"),
                Sales=(sales_col, "sum"),
                Profit=(profit_col, "sum"),
                Avg_Profit_Ratio=(profit_ratio_col, "mean"),
                Avg_Profit_Margin=("Profit Margin %", "mean")
            )
            .reset_index()
            .sort_values("Discount %")
        )

        st.line_chart(
            discount_impact.set_index("Discount %")[
                "Avg_Profit_Margin"
            ]
        )

        st.caption(
            "Higher discount levels can be compared with the "
            "observed average profit margin."
        )

        # ----------------------------------------------------
        # DISCOUNT IMPACT TABLE
        # ----------------------------------------------------

        st.subheader("📊 Discount Impact by Rate")

        display_discount = discount_impact.copy()

        display_discount["Discount %"] = (
            display_discount["Discount %"].map(
                lambda x: f"{x:.0f}%"
            )
        )

        display_discount["Sales"] = (
            display_discount["Sales"]
            .map(lambda x: f"${x:,.2f}")
        )

        display_discount["Profit"] = (
            display_discount["Profit"]
            .map(lambda x: f"${x:,.2f}")
        )

        display_discount["Avg_Profit_Ratio"] = (
            display_discount["Avg_Profit_Ratio"]
            .map(lambda x: f"{x * 100:.2f}%")
        )

        display_discount["Avg_Profit_Margin"] = (
            display_discount["Avg_Profit_Margin"]
            .map(lambda x: f"{x:.2f}%")
        )

        display_discount.columns = [
            "Discount Rate",
            "Orders",
            "Sales",
            "Profit",
            "Avg Profit Ratio",
            "Avg Profit Margin"
        ]

        st.dataframe(
            display_discount,
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------------
        # DISCOUNT AMOUNT vs PROFIT
        # ----------------------------------------------------

        st.subheader("💰 Discount Amount vs Profit")

        amount_profit = (
            discount_df[
                [discount_amount_col, profit_col]
            ]
            .rename(
                columns={
                    discount_amount_col: "Discount Amount",
                    profit_col: "Profit"
                }
            )
            .sort_values("Discount Amount")
        )

        st.scatter_chart(
            amount_profit,
            x="Discount Amount",
            y="Profit"
        )

        # ----------------------------------------------------
        # DISCOUNT RATE FILTER
        # ----------------------------------------------------

        st.subheader("🎚️ Discount Rate Analyzer")

        min_discount = float(
            discount_df[discount_rate_col].min() * 100
        )

        max_discount = float(
            discount_df[discount_rate_col].max() * 100
        )

        selected_discount = st.slider(
            "Select Discount Rate",
            min_value=min_discount,
            max_value=max_discount,
            value=min_discount,
            step=1.0,
            format="%.0f%%"
        )

        selected_discount_df = discount_df[
            discount_df["Discount %"].round(0)
            == round(selected_discount)
        ]

        if not selected_discount_df.empty:

            s1, s2, s3, s4 = st.columns(4)

            s1.metric(
                "Orders",
                f"{len(selected_discount_df):,}"
            )

            s2.metric(
                "Sales",
                f"${selected_discount_df[sales_col].sum():,.2f}"
            )

            s3.metric(
                "Profit",
                f"${selected_discount_df[profit_col].sum():,.2f}"
            )

            selected_margin = (
                selected_discount_df[profit_col].sum()
                / selected_discount_df[sales_col].sum()
                * 100
            )

            s4.metric(
                "Profit Margin",
                f"{selected_margin:.2f}%"
            )

        else:
            st.info(
                "No orders were found at this discount rate."
            )

        # ----------------------------------------------------
        # DISCOUNT IMPACT RATIO
        # ----------------------------------------------------

        st.subheader("📌 Discount Impact Ratio")

        baseline_margin = (
            discount_df[profit_col].sum()
            / discount_df[sales_col].sum()
        )

        if baseline_margin != 0:

            discount_impact["Discount Impact Ratio"] = (
                discount_impact["Avg_Profit_Margin"] / 100
                / baseline_margin
            )

            impact_chart = (
                discount_impact
                .set_index("Discount %")[
                    "Discount Impact Ratio"
                ]
            )

            st.bar_chart(impact_chart)

            st.caption(
                "A ratio above 1 indicates an observed profit "
                "margin above the overall filtered baseline; "
                "a ratio below 1 indicates it is below the baseline."
            )

        # ----------------------------------------------------
        # WHAT-IF DISCOUNT ANALYSIS
        # ----------------------------------------------------

        st.subheader("🔮 What-If Discount Analysis")

        what_if_discount = st.slider(
            "Choose a hypothetical discount",
            min_value=0.0,
            max_value=25.0,
            value=10.0,
            step=1.0,
            format="%.0f%%"
        )

        current_discount = (
            discount_df[discount_rate_col].mean() * 100
        )

        current_profit = discount_df[profit_col].sum()
        total_sales = discount_df[sales_col].sum()

        # Simplified scenario estimate
        discount_change = (
            current_discount - what_if_discount
        ) / 100

        estimated_profit = (
            current_profit
            + total_sales * discount_change
        )

        estimated_difference = (
            estimated_profit - current_profit
        )

        w1, w2, w3 = st.columns(3)

        w1.metric(
            "Current Avg. Discount",
            f"{current_discount:.2f}%"
        )

        w2.metric(
            "Scenario Discount",
            f"{what_if_discount:.0f}%"
        )

        w3.metric(
            "Estimated Profit Change",
            f"${estimated_difference:,.2f}"
        )

        st.info(
            "What-if analysis is a simplified scenario estimate. "
            "It does not establish a causal relationship between "
            "discounts and profit."
        )

# ============================================================
# MARKET & SHIPPING ANALYSIS
# ============================================================

with tab5:

    st.subheader("🌎 Market & Regional Analysis")

    # --------------------------------------------------------
    # MARKET PERFORMANCE
    # --------------------------------------------------------

    st.subheader("🌎 Market Performance")

    market_analysis = (
        filtered_df
        .groupby("Market")
        .agg(
            Orders=("Market", "size"),
            Sales=("Sales", "sum"),
            Profit=("Order Profit Per Order", "sum")
        )
        .reset_index()
    )

    market_analysis["Profit Margin %"] = (
        market_analysis["Profit"]
        / market_analysis["Sales"].replace(0, pd.NA)
    ) * 100

    market_analysis = market_analysis.sort_values(
        "Profit",
        ascending=False
    )

    # Display formatted table
    market_display = market_analysis.copy()

    market_display["Sales"] = market_display["Sales"].map(
        lambda x: f"${x:,.2f}"
    )

    market_display["Profit"] = market_display["Profit"].map(
        lambda x: f"${x:,.2f}"
    )

    market_display["Profit Margin %"] = (
        market_display["Profit Margin %"]
        .map(lambda x: f"{x:.2f}%")
    )

    st.dataframe(
        market_display,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # MARKET PROFIT CHART
    # --------------------------------------------------------

    st.subheader("📊 Profit by Market")

    st.bar_chart(
        market_analysis.set_index("Market")["Profit"]
    )

    st.divider()

    # --------------------------------------------------------
    # COUNTRY PERFORMANCE
    # --------------------------------------------------------

    st.subheader("🌐 Country Performance")

    if "Order Country" in filtered_df.columns:

        country_analysis = (
            filtered_df
            .groupby("Order Country")
            .agg(
                Orders=("Order Country", "size"),
                Sales=("Sales", "sum"),
                Profit=("Order Profit Per Order", "sum")
            )
            .reset_index()
        )

        country_analysis["Profit Margin %"] = (
            country_analysis["Profit"]
            / country_analysis["Sales"].replace(0, pd.NA)
        ) * 100

        country_analysis = country_analysis.sort_values(
            "Profit",
            ascending=False
        )

        # Top 15 countries
        top_countries = country_analysis.head(15)

        country_display = top_countries.copy()

        country_display["Sales"] = country_display["Sales"].map(
            lambda x: f"${x:,.2f}"
        )

        country_display["Profit"] = country_display["Profit"].map(
            lambda x: f"${x:,.2f}"
        )

        country_display["Profit Margin %"] = (
            country_display["Profit Margin %"]
            .map(lambda x: f"{x:.2f}%")
        )

        st.dataframe(
            country_display,
            use_container_width=True,
            hide_index=True
        )

        # Country profit chart
        st.subheader("💰 Top 15 Countries by Profit")

        st.bar_chart(
            top_countries.set_index("Order Country")["Profit"]
        )

    else:
        st.warning(
            "Order Country column was not found in the dataset."
        )

    st.divider()

    # --------------------------------------------------------
    # SALES VS PROFIT
    # --------------------------------------------------------

    st.subheader("📈 Sales vs Profit Analysis")

    sales_profit = (
        filtered_df
        .groupby("Market")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Order Profit Per Order", "sum")
        )
        .reset_index()
    )

    st.scatter_chart(
        sales_profit,
        x="Sales",
        y="Profit",
        size="Sales"
    )

    st.caption(
        "Each point represents a market. "
        "The chart compares total sales with total profit "
        "for the currently selected filters."
    )

    # ------------------------------------------------------------
# HIGH REVENUE BUT WEAK PROFIT MARKETS
# ------------------------------------------------------------

st.subheader("⚠️ High Revenue but Weak Profit Markets")

# Calculate profit margin for each market
sales_profit["Profit Margin %"] = (
    sales_profit["Profit"]
    / sales_profit["Sales"].replace(0, pd.NA)
) * 100

# Use median values as relative thresholds
sales_threshold = sales_profit["Sales"].median()
margin_threshold = sales_profit["Profit Margin %"].median()

weak_profit_markets = sales_profit[
    (sales_profit["Sales"] >= sales_threshold)
    & (sales_profit["Profit Margin %"] < margin_threshold)
].copy()

if not weak_profit_markets.empty:

    weak_profit_markets = weak_profit_markets.sort_values(
        "Sales",
        ascending=False
    )

    weak_profit_markets["Sales"] = weak_profit_markets["Sales"].map(
        lambda x: f"${x:,.2f}"
    )

    weak_profit_markets["Profit"] = weak_profit_markets["Profit"].map(
        lambda x: f"${x:,.2f}"
    )

    weak_profit_markets["Profit Margin %"] = weak_profit_markets[
        "Profit Margin %"
    ].map(
        lambda x: f"{x:.2f}%"
    )

    st.dataframe(
        weak_profit_markets[
            [
                "Market",
                "Sales",
                "Profit",
                "Profit Margin %"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Markets shown have sales at or above the median market sales "
        "but profit margins below the median market margin."
    )

else:

    st.info(
        "No high-revenue, weak-profit markets were identified "
        "for the currently selected filters."
    )

    st.divider()

    # --------------------------------------------------------
    # REGIONAL PROFITABILITY
    # --------------------------------------------------------

    st.subheader("📍 Regional Profitability")

    if "Order Region" in filtered_df.columns:

        region_analysis = (
            filtered_df
            .groupby("Order Region")["Order Profit Per Order"]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(region_analysis)

    else:
        st.warning(
            "Order Region column was not found in the dataset."
        )

    st.divider()

    # --------------------------------------------------------
    # SHIPPING MODE PERFORMANCE
    # --------------------------------------------------------

    st.subheader("🚚 Shipping Mode Performance")

    shipping_analysis = (
        filtered_df
        .groupby("Shipping Mode")
        .agg(
            Orders=("Shipping Mode", "size"),
            Sales=("Sales", "sum"),
            Profit=("Order Profit Per Order", "sum")
        )
        .reset_index()
    )

    shipping_analysis["Profit Margin %"] = (
        shipping_analysis["Profit"]
        / shipping_analysis["Sales"].replace(0, pd.NA)
    ) * 100

    shipping_display = shipping_analysis.copy()

    shipping_display["Sales"] = shipping_display["Sales"].map(
        lambda x: f"${x:,.2f}"
    )

    shipping_display["Profit"] = shipping_display["Profit"].map(
        lambda x: f"${x:,.2f}"
    )

    shipping_display["Profit Margin %"] = (
        shipping_display["Profit Margin %"]
        .map(lambda x: f"{x:.2f}%")
    )

    st.dataframe(
        shipping_display,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("🚚 Profit by Shipping Mode")

    st.bar_chart(
        shipping_analysis.set_index("Shipping Mode")["Profit"]
    )