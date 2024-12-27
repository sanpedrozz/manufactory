from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.alarm.schemas import Alarm
from src.api.alarm.services import alarm_message, add_alarm_history
from src.database import get_db

router = APIRouter()


@router.post("/send_alarm", summary="Отправка аварий",
             description="Этот эндпоинт отправляет аварию и сохраняет её в базе данных.", response_model=Alarm)
async def send_alarm(alarm: Alarm, db: AsyncSession = Depends(get_db)):
    dt = datetime.now()

    try:
        await alarm_message(db, alarm, dt)
        await add_alarm_history(db, alarm, dt)
        return alarm
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
