from fastapi import APIRouter, Request
from services.telegram import send_message
from services.translate import google_trans, deep_trans


router = APIRouter()

@router.post("/hello")
async def hello(request: Request):
    update = await request.json()

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]

        await send_message(chat_id, "Hallo! Ich bin dein deutscher Lernbot 👋")
    
    return {"status": "ok"}

@router.post("/translate")
async def translate(request: Request):
    update = await request.json()

    if "message" in update and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]

        translated_text = google_trans(text, target_lang="de")

        await send_message(chat_id, translated_text)
    
    return {"status": "ok"}
