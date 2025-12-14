import ccxt
import pandas as pd

exchange = ccxt.binance()

PAIRS = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]

def generate_signals():
    results = []

    for pair in PAIRS:
        ohlcv = exchange.fetch_ohlcv(pair, timeframe="1h", limit=200)
        df = pd.DataFrame(ohlcv, columns=["t","o","h","l","c","v"])

        df["ema50"] = df["c"].ewm(span=50).mean()
        df["ema200"] = df["c"].ewm(span=200).mean()

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
