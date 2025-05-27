import streamlit as st
import requests

st.title("API Data Test")

url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
params = {"vs_currency": "usd", "days": "7"}

with st.spinner("Fetching data..."):
    res = requests.get(url, params=params)
    st.write("Status code:", res.status_code)
    if res.status_code == 200:
        data = res.json()
        st.write("Data fetched successfully!")
    else:
        st.error("Failed to fetch data.")

