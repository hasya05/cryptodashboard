import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="💖 Girly Crypto Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for pastel background & styling
st.markdown(
    """
    <style>
    body {
        background-color: #fff0f6;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        color: #d6336c;
        margin: 20px 40px;
    }
    .css-1d391kg {
        background-color: #ffe3ec !important;
        border-radius: 15px;
        padding: 30px 40px;
        box-shadow: 0 8px 20px rgba(214, 51, 108, 0.3);
    }
    .stMetric-value {
        font-size: 3rem !important;
        color: #c61a57 !important;
        font-weight: bold;
    }
    h1, .title {
        font-weight: 900;
        letter-spacing: 0.1em;
    }
    /* Style sidebar */
    .css-1d391kg[data-testid="stSidebar"] {
        background-color: #ffd1dc !important;
        padding: 20px;
        border-radius: 15px;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar widgets for coin and days
coin = st.sidebar.selectbox(
    "Choose cryptocurrency", 
    options=["bitcoin", "ethereum", "dogecoin"],
    index=0
)

days = st.sidebar.slider(
    "Select days of price history", 
    min_value=7, max_value=90, value=7, step=1
)

# Coin icons URLs
coin_icons = {
    "bitcoin": "https://cryptologos.cc/logos/bitcoin-btc-logo.png?v=025",
    "ethereum": "https://cryptologos.cc/logos/ethereum-eth-logo.png?v=025",
    "dogecoin": "https://cryptologos.cc/logos/dogecoin-doge-logo.png?v=025"
}

# Title with icon
st.markdown(
    f"""
    <div style="display:flex; align-items:center; margin-bottom: 20px;">
        <img src="{coin_icons[coin]}" alt="{coin}" width="50" height="50" style="margin-right:10px;">
        <h1>🌸✨ {coin.capitalize()} Crypto Dashboard ✨🌸</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.write(f"Showing price data for **{coin.capitalize()}** over the last **{days} days**.")

# Fetch data with spinner
url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
params = {"vs_currency": "usd", "days": str(days)}

with st.spinner("Fetching data..."):
    res = requests.get(url, params=params)
    if res.status_code != 200:
        st.error("Failed to fetch data from CoinGecko API.")
    else:
        data = res.json()
        prices = data["prices"]
        df = pd.DataFrame(prices, columns=["Time", "Price"])
        df["Time"] = pd.to_datetime(df["Time"], unit="ms")

        # Plotly line chart
        fig = px.line(
            df, x="Time", y="Price",
            title=f"📈 {coin.capitalize()} Price (Last {days} Days)",
            color_discrete_sequence=["#ff77aa"]
        )
        fig.update_layout(
            plot_bgcolor='rgba(255, 240, 246, 0.3)',
            paper_bgcolor='rgba(255, 240, 246, 0.3)',
            font_color='#b3315f',
            title_font=dict(size=24, family="Comic Sans MS, cursive"),
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            hovermode="x unified"
        )

        st.plotly_chart(fig, use_container_width=True)

        latest_price = df.iloc[-1]["Price"]
        st.metric(label=f"💎 Current {coin.capitalize()} Price (USD)", value=f"${latest_price:,.2f}")

st.markdown(
    """
    ---
    Made with 💖 and Python by Hasya | Stay fabulous & code on! 💅
    """,
    unsafe_allow_html=True,
)
