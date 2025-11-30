from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/telegram")
async def telegram_webhook(request: Request):
    data = await request.json()
    # TODO: handle Telegram update
    return {"status": "ok"}
