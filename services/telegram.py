import httpx
import os
import logging

TOKEN = os.getenv("BOT_TOKEN")
BASE = f"https://api.telegram.org/bot{TOKEN}"

async def send_message(chat_id, text):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(f"{BASE}/sendMessage", json={
                    "chat_id": chat_id,
                    "text": text,
                    "parse_mode": "Markdown"
                })
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            logging.error(f"Telegram API error: {e.response.text}")
        except Exception as e:
            logging.error(f"Unexpected error sending message: {e}")