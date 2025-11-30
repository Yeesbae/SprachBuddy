import httpx
import os

TOKEN = os.getenv("BOT_TOKEN")
BASE = f"https://api.telegram.org/bot{TOKEN}"

async def send_message(chat_id, text):
    async with httpx.AsyncClient() as client:
        await client.post(f"{BASE}/sendMessage", json={
            "chat_id": chat_id,
            "text": text
        })
