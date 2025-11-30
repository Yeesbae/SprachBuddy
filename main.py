from fastapi import FastAPI
from api import webhook, health

app = FastAPI()

app.include_router(webhook.router)
app.include_router(health.router)