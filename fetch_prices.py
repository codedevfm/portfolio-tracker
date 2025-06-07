import os
from supabase import create_client
import yfinance as yf

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def update_prices():
    data = supabase.table("portfolio").select("*").execute().data
    for stock in data:
        symbol = stock["symbol"]
        info = yf.Ticker(symbol).info
        price = info.get("regularMarketPrice")
        if price:
            supabase.table("portfolio").update({"price": price}).eq("id", stock["id"]).execute()

if __name__ == "__main__":
    update_prices()