# APL Logistics Profitability Analysis

## 📌 Project Overview

This project analyzes logistics and sales data to understand business profitability, customer performance, product profitability, market performance, and shipping efficiency.

The analysis is performed using Python, Pandas, NumPy, Matplotlib, and Seaborn.

## 📊 Dataset

The dataset contains **180,519 records and 40 columns** related to orders, customers, products, sales, profit, shipping, and delivery.

### Key Information

- Total Sales: 36,778,474.31
- Total Order Profit: 3,966,902.97
- Average Order Profit: 21.97
- Records: 180,519
- Columns: 40

## 🔍 Analysis Performed

### 1. Exploratory Data Analysis

- Dataset structure and data types
- Missing value analysis
- Duplicate record detection
- Categorical value analysis
- Numerical statistics

### 2. Market Profitability

Profitability was analyzed across:

- Europe
- LATAM
- Pacific Asia
- USCA
- Africa

### 3. Customer Segment Analysis

Customer segments analyzed:

- Consumer
- Corporate
- Home Office

### 4. Shipping Analysis

Shipping modes analyzed:

- Standard Class
- Second Class
- First Class
- Same Day

### 5. Product Profitability

The project identifies:

- Top 10 most profitable products
- Bottom 10 least profitable products
- Profitability by product category

### 6. Data Visualization

The project creates visualizations for:

- Profit by Market
- Profit by Customer Segment
- Profit by Shipping Mode
- Top 10 Profitable Products
- Bottom 10 Profitable Products

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook
- Git & GitHub

## 📁 Project Structure

```text
APL_Logistics_Profitability_Analysis/
│
├── app/
│
├── data/
│   └── APL_Logistics.csv
│
├── images/
│   ├── profit_by_market.png
│   ├── profit_by_customer_segment.png
│   ├── profit_by_shipping_mode.png
│   ├── top_10_profitable_products.png
│   └── bottom_10_profitable_products.png
│
├── notebooks/
│   ├── 01_eda.py
│   ├── 02_product_analysis.py
│   └── 03_visualizations.py
│
├── reports/
│   └── profitability_report.md
│
├── .gitignore
└── README.md
```
