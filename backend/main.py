# backend/main.py
from fastapi import FastAPI
from signals import generate_signals

app = FastAPI(title="Crypto Signal Engine")

@app.get("/")
def home():
    return {"status": "Crypto signal engine running"}

@app.get("/signals")
def signals():
    try:
        data = generate_signals()
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "error": str(e)}
