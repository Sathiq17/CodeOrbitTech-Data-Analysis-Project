"""
TASK 2: Sales Data Analysis with Pandas
-----------------------------------------
Input : sample_sales_cleaned.csv
Output: sales_summary_report.md   (short written report)
        by_region.csv, by_product.csv, by_month.csv  (grouped summaries,
        also reused later to build the Excel pivot tables / dashboard)
"""
import pandas as pd

df = pd.read_csv("/home/claude/project/sample_sales_cleaned.csv", parse_dates=["OrderDate"])

# ---- Key metrics ----
total_sales = df["Revenue"].sum()
total_orders = df["OrderID"].nunique()
avg_order_value = df["Revenue"].mean()
total_units = df["Quantity"].sum()

top_products = (
    df.groupby("Product")["Revenue"].sum().sort_values(ascending=False).head(5)
)

# ---- Group summaries ----
by_region = df.groupby("Region").agg(
    Total_Revenue=("Revenue", "sum"),
    Orders=("OrderID", "nunique"),
    Avg_Order_Value=("Revenue", "mean"),
).round(2).sort_values("Total_Revenue", ascending=False)

by_product = df.groupby("Product").agg(
    Total_Revenue=("Revenue", "sum"),
    Units_Sold=("Quantity", "sum"),
    Orders=("OrderID", "nunique"),
).round(2).sort_values("Total_Revenue", ascending=False)

df["Month"] = df["OrderDate"].dt.to_period("M").astype(str)
by_month = df.groupby("Month").agg(
    Total_Revenue=("Revenue", "sum"),
    Orders=("OrderID", "nunique"),
).round(2).sort_index()

by_region.to_csv("/home/claude/project/by_region.csv")
by_product.to_csv("/home/claude/project/by_product.csv")
by_month.to_csv("/home/claude/project/by_month.csv")

# ---- Short written report ----
report = f"""# Sales Data Analysis - Summary Report

**Dataset:** sample_sales_cleaned.csv ({len(df)} orders)

## Key Metrics
- **Total Sales Revenue:** ₹{total_sales:,.2f}
- **Total Orders:** {total_orders}
- **Average Order Value:** ₹{avg_order_value:,.2f}
- **Total Units Sold:** {int(total_units)}

## Top 5 Products by Revenue
{top_products.to_string()}

## Revenue by Region
{by_region.to_string()}

## Monthly Revenue Trend
{by_month.to_string()}

## Observations
- {by_region.index[0]} is the top-performing region by revenue.
- {by_product.index[0]} is the best-selling product by revenue.
- Revenue trend across months is shown above; use this to spot seasonality.
"""

with open("/home/claude/project/sales_summary_report.md", "w") as f:
    f.write(report)

print(report)
