import asyncio
import logging

from fastapi import FastAPI

from services.plc_reader.src.core.reader import Reader
from services.plc_reader.src.routers import routers
from services.plc_reader.src.utils import get_places_by_status
from shared.db.manufactory.models import PlaceStatus
from shared.logger import logger

logging.getLogger("app").setLevel(logging.DEBUG)

app = FastAPI(title="PLC API", version="1.0.0")

# Подключаем маршруты
app.include_router(routers.router)


async def initialize_readers():
    places = await get_places_by_status(PlaceStatus.ACTIVE)

    if not places:
        logger.info("Нет подходящих PLC для подключения.")
        return
    tasks = []

    for place in places:
        logger.info(f"Инициализация Reader для {place.name} ({place.ip})")

        reader = Reader(ip=place.ip)
        tasks.append(reader.run())

    results = await asyncio.gather(*tasks, return_exceptions=True)
    for result in results:
        if isinstance(result, Exception):
            logger.error(f"Ошибка в задаче: {result}")


@app.on_event("startup")
async def on_startup():
    logger.info("Приложение запускается, инициализация PLC...")
    await initialize_readers()
