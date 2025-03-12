import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression 
import numpy as np 

st.title("Grocery Store Sales & Inventory Optimization")  

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Sales Analysis", "Inventory", "Forecasting"])

uploaded_file = st.sidebar.file_uploader("Upload your sales and inventory data (CSV)", type=["csv"])

if uploaded_file: 
    df = pd.read_csv(uploaded_file) 
  
    df["Date"] = pd.to_datetime(df["Date"])

    sales_col = st.sidebar.selectbox("Select Sales Column", df.columns)
    inventory_col = st.sidebar.selectbox("Select Inventory Column", df.columns)
    date_col = st.sidebar.selectbox("Select Date Column", df.columns)

    category_col = st.sidebar.selectbox("Select Category Column (if available)", [None] + list(df.columns))
    region_col = st.sidebar.selectbox("Select Region Column (if available)", [None] + list(df.columns))
    product_col = st.sidebar.selectbox("Select Product Column (if available)", [None] + list(df.columns))

    if sales_col and inventory_col and date_col: 
        df = df.sort_values(by=date_col)

        if page == "Home":
            st.subheader("Data Preview")
            st.dataframe(df.head())

            total_sales = df[sales_col].sum()
            total_inventory = df[inventory_col].sum()

            col1, col2 = st.columns(2)
            col1.metric("Total Sales", f"${total_sales:,.2f}")
            col2.metric("Total Inventory", f"{total_inventory:,} units")

        elif page == "Sales Analysis":
            st.subheader("Sales Trend Over Time")
            
            filtered_df = df.copy()
            if category_col and category_col in df.columns:
                category_filter = st.sidebar.multiselect("Filter by Category", df[category_col].unique())
                if category_filter:
                    filtered_df = filtered_df[filtered_df[category_col].isin(category_filter)]
            
            if region_col and region_col in df.columns:
                region_filter = st.sidebar.multiselect("Filter by Region", df[region_col].unique())
                if region_filter:
                    filtered_df = filtered_df[filtered_df[region_col].isin(region_filter)]
            
            if product_col and product_col in df.columns:
                product_filter = st.sidebar.multiselect("Filter by Product", df[product_col].unique())
                if product_filter:
                    filtered_df = filtered_df[filtered_df[product_col].isin(product_filter)]
            
            fig = px.line(filtered_df, x=date_col, y=sales_col, title="Sales Over Time")
            st.plotly_chart(fig)

        elif page == "Inventory":
            st.subheader("Low Inventory Alerts") 
            threshold = 500
            low_stock = df[df[inventory_col] < threshold]

            if not low_stock.empty:
                st.warning(f"{len(low_stock)} items need restocking!")
                st.dataframe(low_stock) 
            else:
                st.success("All inventory is at a safe level.") 

        elif page == "Forecasting": 
            st.subheader("Sales Forecast (Next 7 Days)")

            df["Days"] = (df[date_col] - df[date_col].min()).dt.days
            X = df[["Days"]] 
            y = df[sales_col]

            model = LinearRegression()
            model.fit(X, y)

            future_days = np.array(range(df["Days"].max() + 1, df["Days"].max() + 8)).reshape(-1, 1)
            future_sales = model.predict(future_days)

            future_dates = pd.date_range(df[date_col].max() + pd.Timedelta(days=1), periods=7)
            forecast_df = pd.DataFrame({date_col: future_dates, "Predicted Sales": future_sales})

            st.dataframe(forecast_df)

            fig_forecast = px.line(forecast_df, x=date_col, y="Predicted Sales", title="Predicted Sales for Next 7 Days")
            st.plotly_chart(fig_forecast)
