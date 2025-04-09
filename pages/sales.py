import streamlit as st
import pandas as pd

st.title("📊 Sales Data")

uploaded_file = st.file_uploader("Upload Sales Data (CSV)", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    st.bar_chart(df.groupby("Date")["Sales"].sum())
