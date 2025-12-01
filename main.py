from fastapi import FastAPI
from api import webhook, health
import os

app = FastAPI()

TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"


app.include_router(webhook.router)
app.include_router(health.router)