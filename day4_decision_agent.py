import requests
from transformers import pipeline

# ----------------------------
# Step 1: Fetch crypto data
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
# Step 2: Deterministic Decision Logic (Python Brain)
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
# Step 3: Initialize LLM (Explanation Brain)
# ----------------------------
generator = pipeline("text2text-generation", model="google/flan-t5-base")


# ----------------------------
# Step 4: Agent Execution
# ----------------------------
def run_agent():
    data = fetch_crypto_data()
    btc, eth, condition, alt_pressure = analyze_market(data)

    print("========== MARKET DATA ==========")
    print(f"Bitcoin: ${btc}")
    print(f"Ethereum: ${eth}")
    print(f"Market Condition: {condition}")

    print("\n========== AI EXPLANATION ==========")

    pressure_text = "Yes" if alt_pressure else "No"

    prompt = f"""
You are a senior crypto market strategist.

Bitcoin is currently priced at {btc}.
Ethereum is currently priced at {eth}.
The overall market condition has been classified as {condition}.
Is Ethereum under 2000? {pressure_text}.

Write a professional market explanation in 4-5 sentences.
Include:
- What the Bitcoin price suggests
- What Ethereum's position suggests
- Overall market sentiment
- Mention altcoin pressure only if Ethereum is below 2000
"""

    response = generator(prompt, max_new_tokens=120, do_sample=False)
    print(response[0]["generated_text"])


# ----------------------------
# Run agent
# ----------------------------
if __name__ == "__main__":
    run_agent()