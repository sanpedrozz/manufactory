from datetime import datetime

from fastapi import APIRouter, HTTPException

from services.alarm.src.models import Alarm
from services.alarm.src.utils import send_alarm_to_telegram, add_alarm_to_db

router = APIRouter()


@router.post("/send_alarm", summary="Отправка аварий",
             description="Этот эндпоинт отправляет аварию и сохраняет её в базе данных.", response_model=Alarm)
async def send_alarm(alarm: Alarm):
    dt = datetime.now()

    try:
        await send_alarm_to_telegram(alarm, dt)
        await add_alarm_to_db(alarm, dt)
        return alarm
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", summary="Главная страница", description="Отображает текст Alarms.")
async def home():
    return {"message": "Alarms"}
