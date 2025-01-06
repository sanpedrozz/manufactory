import logging

from fastapi import FastAPI

from services.plc_reader.src.routers import routers
from services.plc_reader.src.utils import get_places_with_name_containing
from shared.logger import logger

logging.getLogger("app").setLevel(logging.DEBUG)

app = FastAPI(title="PLC API", version="1.0.0")

# Подключаем маршруты
app.include_router(routers.router)


async def initialize_readers():
    places = await get_places_with_name_containing("Кромочник")

    if not places:
        logger.info("Нет подходящих PLC для подключения.")
        return

    for place in places:
        logger.info(f"Инициализация Reader для {place.name} ({place.ip})")


@app.on_event("startup")
async def on_startup():
    logger.info("Приложение запускается, инициализация PLC...")
    await initialize_readers()
