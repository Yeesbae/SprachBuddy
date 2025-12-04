from fastapi import FastAPI
from api import webhook
import os
import logging
import httpx

app = FastAPI()
logger = logging.getLogger("uvicorn")

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

TELEGRAM_API = f"{BASE_URL}/setWebhook"

app.include_router(webhook.router)

@app.on_event("startup")
async def set_telegram_webhook():
    """Automatically sets the Telegram webhook on container startup."""
    if not BOT_TOKEN or not WEBHOOK_URL:
        logger.error("BOT_TOKEN or WEBHOOK_URL is not set.")
        return

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(TELEGRAM_API, json={"url": WEBHOOK_URL})
            if response.status_code == 200:
                logger.info(f"Webhook successfully set to: {WEBHOOK_URL}")
            else:
                logger.error(
                    f"Failed to set webhook: {response.status_code} - {response.text}"
                )
        except Exception as e:
            logger.exception(f"Exception while setting webhook: {e}")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
