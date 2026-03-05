import requests
import json
from datetime import datetime
from transformers import pipeline
import os
import math

# ----------------------------
# Step 1: Fetch crypto data
# ----------------------------
def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin,ethereum", "vs_currencies": "usd"}
    response = requests.get(url, params=params)
    return response.json()

# ----------------------------
# Step 2: Load previous prices
# ----------------------------
def load_previous_prices(filename="prev_prices.json"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}

# ----------------------------
# Step 3: Save current prices
# ----------------------------
def save_current_prices(data, filename="prev_prices.json"):
    with open(filename, "w") as f:
        json.dump(data, f)

# ----------------------------
# Step 4: Calculate % change
# ----------------------------
def calculate_change(current, previous):
    changes = {}
    for coin in current:
        if coin in previous:
            old = previous[coin]["usd"]
            new = current[coin]["usd"]
            percent = ((new - old) / old) * 100
            changes[coin] = round(percent, 2)
        else:
            changes[coin] = 0.0
    return changes

# ----------------------------
# Step 5: Draw log-scaled ASCII chart
# ----------------------------
def draw_ascii_chart(data):
    max_length = 30
    max_price = max([c["usd"] for c in data.values()])
    print("========== PRICE CHART ==========")
    for coin, info in data.items():
        # Use log scale to show smaller coins
        bar_length = max(1, int(math.log(info["usd"] + 1) / math.log(max_price + 1) * max_length))
        bar = "█" * bar_length
        print(f"{coin.capitalize():<8} | {bar} ${info['usd']}")
    print("="*40)

# ----------------------------
# Step 6: Create report
# ----------------------------
def create_report(data, changes):
    btc_price = data["bitcoin"]["usd"]
    eth_price = data["ethereum"]["usd"]
    btc_change = changes.get("bitcoin", 0)
    eth_change = changes.get("ethereum", 0)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = f"""
Crypto Market Report ({now}):
- Bitcoin: ${btc_price} ({btc_change}% change)
- Ethereum: ${eth_price} ({eth_change}% change)
"""
    return report

# ----------------------------
# Step 7: Initialize AI model
# ----------------------------
generator = pipeline("text2text-generation", model="google/flan-t5-base")

# ----------------------------
# Step 8: Run agent
# ----------------------------
def run_agent():
    current_data = fetch_crypto_data()
    previous_data = load_previous_prices()
    changes = calculate_change(current_data, previous_data)

    report = create_report(current_data, changes)

    # Print raw report
    print("========== RAW REPORT ==========")
    print(report.strip())

    # Draw ASCII chart
    draw_ascii_chart(current_data)

    # AI prompt for real analysis
    prompt = f"""
You are a professional crypto market analyst.

Based on the report below:

{report}

Please provide:
1. A short market summary in 2–3 sentences (do NOT repeat the report).
2. A one-sentence market insight highlighting trends or investor sentiment.
3. Mention Bitcoin and Ethereum separately with context, not just numbers.
"""

    # Generate AI analysis
    response = generator(prompt, max_new_tokens=150, do_sample=False)
    ai_summary = response[0]["generated_text"].strip()

    print("========== AI ANALYSIS ==========")
    print(ai_summary)

    # Optional quick one-line insight
    quick_insight = ai_summary.split("\n")[0]
    print("\nQuick Market Insight:", quick_insight)

    # Save current prices for next % change
    save_current_prices(current_data)

# ----------------------------
# Step 9: Execute
# ----------------------------
if __name__ == "__main__":
    run_agent()