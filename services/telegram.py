import httpx
import os
import logging

TOKEN = os.getenv("BOT_TOKEN")
BASE = f"https://api.telegram.org/bot{TOKEN}"

async def send_message(chat_id, text, message_thread_id=None):
    """
    Send a message to a Telegram chat.
    
    Args:
        chat_id: The chat ID to send the message to
        text: The message text
        message_thread_id: Optional. The topic/forum thread ID to reply to
    """
    async with httpx.AsyncClient() as client:
        try:
            payload = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "Markdown"
            }
            
            # Add message_thread_id if provided (for forum topics/threads)
            if message_thread_id is not None:
                payload["message_thread_id"] = message_thread_id
            
            resp = await client.post(f"{BASE}/sendMessage", json=payload)
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            logging.error(f"Telegram API error: {e.response.text}")
        except Exception as e:
            logging.error(f"Unexpected error sending message: {e}")
