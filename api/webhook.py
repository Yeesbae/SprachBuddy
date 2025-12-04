from fastapi import APIRouter, Request
from services.telegram import send_message
from services.translate import google_trans, deep_trans


router = APIRouter()

@router.post("/telegram")
async def telegram_webhook(request: Request):
    update = await request.json()
    
    if "message" not in update or "text" not in update["message"]:
        return {"status": "ok"}

    chat_id = update["message"]["chat"]["id"]
    text = update["message"]["text"]

    if text.startswith("/hello"):
        await send_message(chat_id, "Hallo! Ich bin dein deutscher Lernbot 👋")
    elif text.startswith("/health"):
        # await send_message(chat_id, "✅ Der Bot ist aktiv und funktionsfähig.")
        await send_message(chat_id, "✅ The bot is active and operational.")
    elif text.startswith("/translate"):
        user_text = text.removeprefix("/translate").strip()
        if not user_text:
            await send_message(chat_id, "❌ Please provide text to translate, e.g. `/translate Hello`.")
        else:
            translated_text_google = await google_trans(user_text, target_lang="de")
            translated_text_deep = deep_trans(user_text, target_lang="de")
            
            reply_message = (
                f"📌 *Original:*\n{user_text}\n\n"
                f"🌐 *Google Translate:*\n{translated_text_google}\n\n"
                f"🔁 *Deep Translator:*\n{translated_text_deep}"
            )
            await send_message(chat_id, reply_message)
    else:
        # await send_message(chat_id, "❌ Unrecognized command.")
        translated_text_google = await google_trans(text, target_lang="de")
        translated_text_deep = deep_trans(text, target_lang="de")
        
        reply_message = (
            f"📌 *Original:*\n{text}\n\n"
            f"🌐 *Google Translate:*\n{translated_text_google}\n\n"
            f"🔁 *Deep Translator:*\n{translated_text_deep}"
        )
        await send_message(chat_id, reply_message)
    
    return {"status": "ok"}
