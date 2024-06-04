import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Visualization", layout="wide")
st.title("Data Overview")

df = pd.read_csv("MARKET_Car_Prices_clean.csv")

# Data overview
st.table(df.head())
