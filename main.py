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
async def read_portfolio(request: Request):
    response = supabase.table("portfolio").select("*").execute()
    portfolio = response.data
    return templates.TemplateResponse("index.html", {"request": request, "portfolio": portfolio})


@app.post("/add-stock", response_class=HTMLResponse)
async def add_stock(
    symbol: str = Form(...),
    buy_date: str = Form(...),
    buy_price: float = Form(...),
    quantity: float = Form(...)
):
    supabase.table("portfolio").insert({
        "symbol": symbol.upper(),
        "buy_date": buy_date,
        "buy_price": buy_price,
        "quantity": quantity
    }).execute()

    response = supabase.table("portfolio").select("*").execute()
    portfolio = response.data
    # We don't need Request here because we're returning a partial, but Jinja2Templates needs it.
    # So we'll create a dummy Request or adjust the template to not use it (no `request` used in partial).
    # To keep it simple, we'll pass a dummy Request:

    from starlette.requests import Request as StarletteRequest
    dummy_scope = {"type": "http"}
    dummy_request = StarletteRequest(dummy_scope)

    return templates.TemplateResponse("partials/portfolio_table.html", {"request": dummy_request, "portfolio": portfolio})
