import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📈 Data Analytics")

uploaded_file = st.file_uploader("Upload Data for Analysis (CSV)", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    fig = px.line(df, x="Date", y="Sales", title="Sales Over Time")
    st.plotly_chart(fig)
