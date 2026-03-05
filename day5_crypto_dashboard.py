import streamlit as st
import requests
import pandas as pd
from transformers import pipeline

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="Crypto AI Dashboard", layout="centered")
st.title("🚀 Crypto AI Market Dashboard")

# ----------------------------
# Fetch Current Crypto Data
# ----------------------------
def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum",
        "vs_currencies": "usd"
    }
    response = requests.get(url, params=params)
    return response.json()

# ----------------------------
# Fetch 7-Day Bitcoin History
# ----------------------------
def fetch_bitcoin_history():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "7"
    }

    response = requests.get(url, params=params)
    data = response.json()

    prices = data["prices"]
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    return df

# ----------------------------
# Decision Logic (Python Brain)
# ----------------------------
def analyze_market(data):
    btc = data["bitcoin"]["usd"]
    eth = data["ethereum"]["usd"]

    if btc > 60000:
        market_condition = "Bullish"
    elif btc < 30000:
        market_condition = "Bearish"
    else:
        market_condition = "Neutral"

    altcoin_pressure = eth < 2000

    return btc, eth, market_condition, altcoin_pressure

# ----------------------------
# Load LLM (cached)
# ----------------------------
@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model="google/flan-t5-base")

generator = load_model()

# ----------------------------
# Refresh Button
# ----------------------------
st.button("🔄 Refresh Market Data")

# ----------------------------
# Run Dashboard Logic
# ----------------------------
data = fetch_crypto_data()
btc, eth, condition, alt_pressure = analyze_market(data)

st.subheader("📊 Live Market Data")
st.write(f"**Bitcoin:** ${btc}")
st.write(f"**Ethereum:** ${eth}")

if condition == "Bullish":
    st.success(f"Market Condition: {condition}")
elif condition == "Bearish":
    st.error(f"Market Condition: {condition}")
else:
    st.warning(f"Market Condition: {condition}")

# ----------------------------
# Bitcoin Chart
# ----------------------------
st.subheader("📈 Bitcoin 7-Day Price Trend")
btc_history = fetch_bitcoin_history()
st.line_chart(btc_history.set_index("timestamp")["price"])

# ----------------------------
# AI Explanation
# ----------------------------
st.subheader("🤖 AI Market Analysis")

pressure_text = "Yes" if alt_pressure else "No"

prompt = f"""
You are a senior crypto market strategist.

Bitcoin is currently priced at {btc}.
Ethereum is currently priced at {eth}.
The overall market condition has been classified as {condition}.
Is Ethereum under 2000? {pressure_text}.

Write a professional explanation in 4-5 sentences.
Mention altcoin pressure only if Ethereum is below 2000.
"""

response = generator(prompt, max_new_tokens=120, do_sample=False)
st.write(response[0]["generated_text"])