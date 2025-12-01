from fastapi import FastAPI
from api import webhook, health
import os

app = FastAPI()

TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"


app.include_router(webhook.router)
app.include_router(health.router)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)