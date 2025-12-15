from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from .signals import generate_signals  # <-- relative import

app = FastAPI(title="Crypto Signal Engine")

templates = Jinja2Templates(directory="templates")

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

@app.get("/dashboard")
def dashboard(request: Request):
    try:
        signals_data = generate_signals()
        return templates.TemplateResponse("dashboard.html", {"request": request, "signals": signals_data})
    except Exception as e:
        return templates.TemplateResponse("dashboard.html", {"request": request, "signals": [], "error": str(e)})
