import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np


st.title("📊") 
from PIL import Image 

image = Image.open("dash.png")
st.image(image, caption="Dashboard Preview",  use_container_width =True)

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Sales Analysis", "Inventory", "Forecasting", "Profit Analysis", "Supplier Performance"])

uploaded_file = st.sidebar.file_uploader("UPLOAD DATA (CSV)", type=["csv"])

if uploaded_file: 
    df = pd.read_csv(uploaded_file) 
  
    df["Date"] = pd.to_datetime(df["Date"])

    with st.sidebar.expander("Select Data Parameter", expanded=False):
        sales_col = st.selectbox("Select Sales", df.columns)
        inventory_col = st.selectbox("Select Inventory ", df.columns)
        date_col = st.selectbox("Select Date ", df.columns)
        cost_col = st.selectbox("Select Cost (if available)", [None] + list(df.columns))
        supplier_col = st.selectbox("Select Supplier (if available)", [None] + list(df.columns))
        category_col = st.selectbox("Select Category (if available)", [None] + list(df.columns))
        region_col = st.selectbox("Select Region (if available)", [None] + list(df.columns))
        product_col = st.selectbox("Select Product (if available)", [None] + list(df.columns))

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
            
            with st.sidebar.expander("Filters", expanded=False):
                category_filter = st.multiselect("Filter by Category", df[category_col].unique()) if category_col else []
                region_filter = st.multiselect("Filter by Region", df[region_col].unique()) if region_col else []
                product_filter = st.multiselect("Filter by Product", df[product_col].unique()) if product_col else []
            
            filtered_df = df.copy()
            if category_filter:
                filtered_df = filtered_df[filtered_df[category_col].isin(category_filter)]
            if region_filter:
                filtered_df = filtered_df[filtered_df[region_col].isin(region_filter)]
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
        
        elif page == "Profit Analysis":
            st.subheader("Profit Margin Analysis")
            if cost_col:
                df["Profit"] = df[sales_col] - df[cost_col]
                df["Profit Margin"] = (df["Profit"] / df[sales_col]) * 100
                
                high_profit = df[df["Profit Margin"] > df["Profit Margin"].median()]
                low_profit = df[df["Profit Margin"] <= df["Profit Margin"].median()]
                
                st.metric("Average Profit Margin", f"{df['Profit Margin'].mean():.2f}%")
                st.subheader("Top High-Profit Items")
                st.dataframe(high_profit.head(10))
                
                st.subheader("Low-Profit Items (Consider Reviewing)")
                st.dataframe(low_profit.head(10))
            else:
                st.warning("Please select a cost column to analyze profit margins.")

        elif page == "Supplier Performance":
            st.subheader("Supplier Performance Tracking")
            if supplier_col:
                supplier_performance = df.groupby(supplier_col)[sales_col].sum().reset_index()
                fig_supplier = px.bar(supplier_performance, x=supplier_col, y=sales_col, title="Supplier Sales Performance")
                st.plotly_chart(fig_supplier)
            else:
                st.warning("Please select a supplier column to track supplier performance.")
