import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

# Streamlit App
st.title("📊 Grocery Store Sales and Inventory Optimization")

# File Upload
uploaded_file = st.file_uploader("Upload your sales and inventory data (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Convert Date column to datetime
    df["Date"] = pd.to_datetime(df["Date"])

    # User selects columns
    sales_col = st.selectbox("Select Sales Column", df.columns)
    inventory_col = st.selectbox("Select Inventory Column", df.columns)
    date_col = st.selectbox("Select Date Column", df.columns)

    if sales_col and inventory_col and date_col:
        # Sort by Date
        df = df.sort_values(by=date_col)

        # Display Data
        st.subheader("📌 Data Preview")
        st.dataframe(df.head())

        # Key Metrics
        total_sales = df[sales_col].sum()
        total_inventory = df[inventory_col].sum()

        col1, col2 = st.columns(2)
        col1.metric("📈 Total Sales", f"${total_sales:,.2f}")
        col2.metric("📦 Total Inventory", f"{total_inventory:,} units")

        # Restock Alerts
        st.subheader("⚠️ Low Inventory Alerts")
        threshold = 500  # Set low stock threshold
        low_stock = df[df[inventory_col] < threshold]
        if not low_stock.empty:
            st.warning(f"🚨 {len(low_stock)} items need restocking!")
            st.dataframe(low_stock)
        else:
            st.success("✅ All inventory is at a safe level.")

        # Sales Trend Chart
        st.subheader("📊 Sales Trend Over Time")
        fig = px.line(df, x=date_col, y=sales_col, title="Sales Over Time")
        st.plotly_chart(fig)

        # Predictive Sales Forecast
        st.subheader("🔮 Sales Forecast (Next 7 Days)")

        # Prepare data for Linear Regression
        df["Days"] = (df[date_col] - df[date_col].min()).dt.days
        X = df[["Days"]]
        y = df[sales_col]

        # Train model
        model = LinearRegression()
        model.fit(X, y)

        # Predict next 7 days
        future_days = np.array(range(df["Days"].max() + 1, df["Days"].max() + 8)).reshape(-1, 1)
        future_sales = model.predict(future_days)

        # Create forecast DataFrame
        future_dates = pd.date_range(df[date_col].max() + pd.Timedelta(days=1), periods=7)
        forecast_df = pd.DataFrame({date_col: future_dates, "Predicted Sales": future_sales})

        # Show forecast data
        st.dataframe(forecast_df)

        # Plot forecast
        fig_forecast = px.line(forecast_df, x=date_col, y="Predicted Sales", title="Predicted Sales for Next 7 Days")
        st.plotly_chart(fig_forecast)
