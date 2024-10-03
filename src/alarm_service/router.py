from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.alarm_service.schemas import Alarm
from src.alarm_service.services import alarm_message
from src.database import get_db

router = APIRouter()


@router.post("/send_alarm", summary="Отправка аварий",
             description="Этот эндпоинт отправляет аварию и сохраняет её в базе данных.", response_model=Alarm)
async def send_alarm(alarm: Alarm, db: AsyncSession = Depends(get_db)):
    try:
        await alarm_message(alarm, db)
        return alarm
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке аварии: {str(e)}")