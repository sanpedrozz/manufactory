import asyncio
import logging

from fastapi import FastAPI

from services.plc_reader.src.core.reader import Reader
from services.plc_reader.src.routers import routers
from services.plc_reader.src.utils import get_places_by_status
from shared.db.manufactory.models import Place, PlaceStatus
from shared.logger import logger

logging.getLogger("app").setLevel(logging.DEBUG)

app = FastAPI(title="PLC API", version="1.0.0")

# Подключаем маршруты
app.include_router(routers.router)

#
plc_readers = {}


@app.on_event("startup")
async def on_startup():
    global plc_readers

    logger.info("Приложение запускается, инициализация PLC...")

    places = await get_places_by_status(PlaceStatus.ACTIVE)
    if not places:
        logger.info("Нет подходящих PLC для подключения.")
        return

    for place in places:
        logger.info(f"Инициализация Reader для {place.name} ({place.ip})")
        plc_readers[place.name] = asyncio.create_task(run_readers(place))

    logger.info("Приложение успешно запущено и PLC инициализированы.")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Событие, выполняемое при остановке приложения.
    Завершение работы всех задач.
    """
    global plc_readers
    for name, plc_readers in plc_readers.items():
        plc_readers.cancel()
        logger.info(f"Остановлена обработка задач для роботов с IP: {name}")


async def run_readers(place: Place):
    reader = Reader(place)
    reader.initialize()
    await reader.run()
