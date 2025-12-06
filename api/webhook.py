from fastapi import APIRouter, Request
from services.telegram import send_message
from services.translate import google_trans, deep_trans
from core.config import ALLOWED_TOPIC_IDS
from utils.find_topic_id import print_message_info  # DEBUG: Import helper
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/telegram")
async def telegram_webhook(request: Request):
    update = await request.json()
    
    # Handle both regular messages and channel posts
    message_data = None
    if "message" in update:
        message_data = update["message"]
    elif "channel_post" in update:
        message_data = update["channel_post"]
    
    # Early exit: If no message or channel post, or no text content, ignore silently
    if not message_data or "text" not in message_data:
        return {"status": "ok"}
    
    # Early exit: Filter by topic/channel if configured (BEFORE any logging or processing)
    if ALLOWED_TOPIC_IDS:
        message_thread_id = message_data.get("message_thread_id")
        # If message is not from an allowed topic, ignore it silently (no logs, no processing)
        if message_thread_id not in ALLOWED_TOPIC_IDS:
            return {"status": "ok"}
    
    # Only log and process messages from allowed channels
    logger.info(f"Processing message from allowed channel - thread_id: {message_data.get('message_thread_id')}")
    # print_message_info(update)  # DEBUG: Uncomment to see detailed message info

    chat_id = message_data["chat"]["id"]
    text = message_data["text"]
    message_thread_id = message_data.get("message_thread_id")  # Get topic ID if exists

    if text.startswith("/hello"):
        await send_message(chat_id, "Hallo! Ich bin dein deutscher Lernbot 👋", message_thread_id)
    elif text.startswith("/health"):
        # await send_message(chat_id, "✅ Der Bot ist aktiv und funktionsfähig.")
        await send_message(chat_id, "✅ The bot is active and operational.", message_thread_id)
    elif text.startswith("/translate"):
        user_text = text.removeprefix("/translate").strip()
        if not user_text:
            await send_message(chat_id, "❌ Please provide text to translate, e.g. `/translate Hello`.", message_thread_id)
        else:
            translated_text_google = await google_trans(user_text, target_lang="de")
            translated_text_deep = deep_trans(user_text, target_lang="de")
            
            reply_message = (
                f"📌 *Original:*\n{user_text}\n\n"
                f"🌐 *Google Translate:*\n{translated_text_google}\n\n"
                f"🔁 *Deep Translator:*\n{translated_text_deep}"
            )
            await send_message(chat_id, reply_message, message_thread_id)
    else:
        # await send_message(chat_id, "❌ Unrecognized command.")
        translated_text_google = await google_trans(text, target_lang="de")
        translated_text_deep = deep_trans(text, target_lang="de")
        
        reply_message = (
            f"📌 *Original:*\n{text}\n\n"
            f"🌐 *Google Translate:*\n{translated_text_google}\n\n"
            f"🔁 *Deep Translator:*\n{translated_text_deep}"
        )
        await send_message(chat_id, reply_message, message_thread_id)
    
    return {"status": "ok"}
