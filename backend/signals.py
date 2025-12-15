# backend/signals.py
from fastapi import FastAPI
import pandas as pd
from binance.client import Client
import os

# Load API keys from environment variables
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

client = Client(API_KEY, API_SECRET)

PAIRS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]

app = FastAPI()

def generate_signals():
    results = []

    for pair in PAIRS:
        # Fetch recent candles
        klines = client.get_klines(symbol=pair, interval=Client.KLINE_INTERVAL_1HOUR, limit=200)
        df = pd.DataFrame(klines, columns=["t","o","h","l","c","v","closeTime","qav","numTrades","takerBaseVol","takerQuoteVol","ignore"])
        df["c"] = df["c"].astype(float)

        # EMA calculations
        df["ema50"] = df["c"].ewm(span=50).mean()
        df["ema200"] = df["c"].ewm(span=200).mean()

        # Signal logic
        if df["ema50"].iloc[-1] > df["ema200"].iloc[-1]:
            signal = "BUY"
        elif df["ema50"].iloc[-1] < df["ema200"].iloc[-1]:
            signal = "SELL"
        else:
            signal = "WAIT"

        results.append({
            "pair": pair,
            "signal": signal,
            "price": round(df["c"].iloc[-1], 2)
        })

    return results

# FastAPI endpoint
@app.get("/signals")
def read_signals():
    try:
        return {"success": True, "data": generate_signals()}
    except Exception as e:
        return {"success": False, "error": str(e)}
