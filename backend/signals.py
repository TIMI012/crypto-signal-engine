import pandas as pd
from binance.client import Client
import os

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

client = Client(API_KEY, API_SECRET)
PAIRS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]

def generate_signals():
    results = []
    for pair in PAIRS:
        klines = client.get_klines(symbol=pair, interval=Client.KLINE_INTERVAL_1HOUR, limit=200)
        df = pd.DataFrame(klines, columns=["t","o","h","l","c","v","closeTime","qav","numTrades","takerBaseVol","takerQuoteVol","ignore"])
        df["c"] = df["c"].astype(float)
        df["ema50"] = df["c"].ewm(span=50).mean()
        df["ema200"] = df["c"].ewm(span=200).mean()
        if pd.isna(df["ema50"].iloc[-1]) or pd.isna(df["ema200"].iloc[-1]):
            signal = "WAIT"
        elif df["ema50"].iloc[-1] > df["ema200"].iloc[-1]:
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
