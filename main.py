from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from supabase import create_client
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    response = supabase.table("portfolio").select("*").execute()
    data = response.data
    return templates.TemplateResponse("index.html", {"request": request, "stocks": data})