import streamlit as st
import pandas as pd

st.title("📦 Inventory Management")

uploaded_file = st.file_uploader("Upload Inventory Data (CSV)", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    low_stock = df[df["Stock"] < 10]
    st.warning(f"⚠️ {len(low_stock)} items are running low on stock!")
