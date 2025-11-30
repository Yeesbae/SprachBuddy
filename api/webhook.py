from services.telegram import send_message

@router.post("/telegram")
async def telegram_webhook(request: Request):
    update = await request.json()

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]

        await send_message(chat_id, "Hallo! Ich bin dein deutscher Lernbot 👋")
    
    return {"status": "ok"}
