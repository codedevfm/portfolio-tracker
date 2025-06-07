from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from supabase import create_client, Client
import os

app = FastAPI()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@app.get("/journal", response_class=HTMLResponse)
async def get_journal(request: Request):
    journal = supabase.table("journal").select("*").order("buy_date", desc=True).execute().data
    return templates.TemplateResponse("partials/journal.html", {"request": request, "journal": journal})

@app.post("/journal", response_class=HTMLResponse)
async def add_entry(request: Request,
                    symbol: str = Form(...),
                    buy_date: str = Form(...),
                    buy_price: float = Form(...),
                    quantity: float = Form(...)):
    supabase.table("journal").insert({
        "id": str(uuid.uuid4()),
        "symbol": symbol.upper(),
        "buy_date": buy_date,
        "buy_price": buy_price,
        "quantity": quantity
    }).execute()
    return await get_journal(request)

@app.get("/holdings", response_class=HTMLResponse)
async def get_holdings(request: Request):
    journal = supabase.table("journal").select("*").execute().data
    holdings = {}

    for entry in journal:
        symbol = entry["symbol"]
        if symbol not in holdings:
            holdings[symbol] = {"symbol": symbol, "total_quantity": 0, "total_cost": 0}
        holdings[symbol]["total_quantity"] += entry["quantity"]
        holdings[symbol]["total_cost"] += entry["quantity"] * entry["buy_price"]

    for symbol, data in holdings.items():
        data["avg_buy_price"] = data["total_cost"] / data["total_quantity"]
        current_price = yf.Ticker(symbol).history(period="1d")["Close"].iloc[-1]
        data["current_price"] = current_price
        data["market_value"] = data["total_quantity"] * current_price
        data["pnl"] = data["market_value"] - data["total_cost"]

    return templates.TemplateResponse("partials/holdings.html", {
        "request": request,
        "holdings": list(holdings.values())
    })
