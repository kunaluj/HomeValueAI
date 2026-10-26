
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression

# Page settings
st.set_page_config(
    page_title="Retail Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load actual dataset
DATA_PATH = r"C:\hadoop\retail_sales.csv"

try:
    sales_df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    st.error(f"Dataset not found: {DATA_PATH}")
    st.stop()

# Prepare data
sales_df["Revenue"] = (
    sales_df["Quantity"] * sales_df["UnitPrice"]
)
sales_df["OrderDate"] = pd.to_datetime(sales_df["OrderDate"])

total_revenue = sales_df["Revenue"].sum()
total_orders = sales_df["OrderID"].nunique()
total_products = sales_df["Product"].nunique()

# Dashboard heading
st.title("Retail Sales Forecasting Dashboard")
st.subheader("Big Data Analytics using Hadoop")
st.write(
    "Analyze retail revenue, product performance, "
    "customer purchases, and future sales."
)

# KPI cards
st.divider()
col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Total Orders", f"{total_orders}")
col3.metric("Products", f"{total_products}")

# Product analysis
st.divider()
st.header("1. Product-wise Revenue Analysis")

product_data = (
    sales_df.groupby("Product", as_index=False)["Revenue"]
    .sum()
    .sort_values("Revenue")
)

fig_product = px.bar(
    product_data,
    x="Revenue",
    y="Product",
    orientation="h",
    title="Revenue by Product",
    labels={"Revenue": "Revenue (₹)", "Product": "Product"},
    text="Revenue"
)
st.plotly_chart(fig_product, width="stretch")

# Category analysis
st.divider()
st.header("2. Category-wise Revenue Analysis")

category_data = (
    sales_df.groupby("Category", as_index=False)["Revenue"]
    .sum()
)

fig_category = px.pie(
    category_data,
    names="Category",
    values="Revenue",
    title="Revenue Share by Category",
    hole=0.35
)
st.plotly_chart(fig_category, width="stretch")

# Region analysis
st.divider()
st.header("3. Region-wise Revenue Analysis")

region_data = (
    sales_df.groupby("Region", as_index=False)["Revenue"]
    .sum()
    .sort_values("Revenue")
)

fig_region = px.bar(
    region_data,
    x="Region",
    y="Revenue",
    title="Revenue by Region",
    labels={"Revenue": "Revenue (₹)", "Region": "Region"},
    text="Revenue"
)
st.plotly_chart(fig_region, width="stretch")

st.caption(
    "Dashboard sales metrics are calculated from the original retail CSV. "
    "Hadoop MapReduce outputs are used separately to verify aggregate results."
)

# Customer analysis
st.divider()
st.header("4. Customer Purchase Pattern Analysis")

customer_data = (
    sales_df.groupby("CustomerID")
    .agg(
        Orders=("OrderID", "nunique"),
        TotalSpent=("Revenue", "sum")
    )
    .reset_index()
)

fig_customer = px.bar(
    customer_data.sort_values("Orders"),
    x="Orders",
    y="CustomerID",
    orientation="h",
    title="Number of Orders per Customer",
    text="Orders"
)
st.plotly_chart(fig_customer, width="stretch")

st.subheader("Customer Spending Table")
st.dataframe(
    customer_data.sort_values("TotalSpent", ascending=False),
    width="stretch",
    hide_index=True
)

# Forecasting
st.divider()
st.header("5. Daily Sales Forecasting")

daily_sales = (
    sales_df.groupby("OrderDate", as_index=False)["Revenue"]
    .sum()
    .sort_values("OrderDate")
)

daily_sales["DayNumber"] = range(1, len(daily_sales) + 1)

if len(daily_sales) >= 2:
    model = LinearRegression()
    model.fit(daily_sales[["DayNumber"]], daily_sales["Revenue"])

    future_days = pd.DataFrame({
        "DayNumber": range(
            len(daily_sales) + 1,
            len(daily_sales) + 4
        )
    })

    future_days["ForecastRevenue"] = model.predict(
        future_days[["DayNumber"]]
    )
    future_days["ForecastRevenue"] = (
        future_days["ForecastRevenue"].clip(lower=0)
    )
    future_days["Date"] = pd.date_range(
        start=daily_sales["OrderDate"].max() + pd.Timedelta(days=1),
        periods=3
    )

    history = daily_sales[["OrderDate", "Revenue"]].rename(
        columns={"OrderDate": "Date", "Revenue": "Sales"}
    )
    history["Type"] = "Actual"

    forecast = future_days[["Date", "ForecastRevenue"]].rename(
        columns={"ForecastRevenue": "Sales"}
    )
    forecast["Type"] = "Forecast"

    chart_data = pd.concat([history, forecast], ignore_index=True)

    fig_forecast = px.line(
        chart_data,
        x="Date",
        y="Sales",
        color="Type",
        markers=True,
        title="Actual vs Forecast Daily Revenue",
        labels={"Sales": "Revenue (₹)", "Date": "Date"}
    )
    st.plotly_chart(fig_forecast, width="stretch")

    st.subheader("Forecast for Next 3 Days")
    forecast_display = future_days[["Date", "ForecastRevenue"]].copy()
    forecast_display["ForecastRevenue"] = (
        forecast_display["ForecastRevenue"].round(2)
    )
    st.dataframe(
        forecast_display,
        width="stretch",
        hide_index=True
    )

    st.caption(
        "Forecasts are illustrative estimates based on a small sample "
        "of historical data, not reliable long-term predictions."
    )
else:
    st.warning("At least two days of sales data are needed for forecasting.")

# Hadoop MapReduce Integration
st.divider()
st.header("6. Hadoop MapReduce Results")

st.write(
    "These results are loaded from the output files generated "
    "by Hadoop MapReduce jobs."
)

# Read product revenue output generated by Hadoop
try:
    product_output = pd.read_csv(
        r"C:\hadoop\RetailDashboard\product_revenue.txt",
        sep="\t",
        header=None,
        names=["Product", "Revenue"]
    )

    product_output["Revenue"] = pd.to_numeric(
        product_output["Revenue"], errors="coerce"
    )
    product_output = product_output.dropna(subset=["Revenue"])

    st.subheader("Hadoop: Product-wise Revenue")
    st.dataframe(product_output, width="stretch", hide_index=True)

    fig_hadoop_product = px.bar(
        product_output,
        x="Product",
        y="Revenue",
        title="Product Revenue Calculated by Hadoop",
        labels={"Revenue": "Revenue (₹)"}
    )
    st.plotly_chart(fig_hadoop_product, width="stretch")

except Exception as e:
    st.error(f"Could not load Hadoop product output: {e}")


# Read category and region output generated by Hadoop
try:
    breakdown_output = pd.read_csv(
        r"C:\hadoop\RetailDashboard\sales_breakdown.txt",
        sep=r"\s+",
        header=None,
        names=["Type", "Revenue"],
        engine="python"
    )

    breakdown_output["Revenue"] = pd.to_numeric(
        breakdown_output["Revenue"], errors="coerce"
    )
    breakdown_output = breakdown_output.dropna(subset=["Revenue"])

    category_output = breakdown_output[
        breakdown_output["Type"].str.startswith("CATEGORY:")
    ].copy()
    category_output["Category"] = category_output["Type"].str.replace(
        "CATEGORY:", "", regex=False
    )

    region_output = breakdown_output[
        breakdown_output["Type"].str.startswith("REGION:")
    ].copy()
    region_output["Region"] = region_output["Type"].str.replace(
        "REGION:", "", regex=False
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Hadoop: Category Revenue")
        st.dataframe(
            category_output[["Category", "Revenue"]].style.format(
                {"Revenue": "₹{:,.0f}"}
            ),
            width="stretch",
            hide_index=True
        )

    with col2:
        st.subheader("Hadoop: Region Revenue")
        st.dataframe(
            region_output[["Region", "Revenue"]].style.format(
                {"Revenue": "₹{:,.0f}"}
            ),
            width="stretch",
            hide_index=True
        )

except Exception as e:
    st.error(f"Could not load Hadoop breakdown output: {e}")
