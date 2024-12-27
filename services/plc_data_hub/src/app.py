import asyncio
import logging

# from services.plc_data_hub.src.core.plc_reader import Reader
from services.plc_data_hub.src.core.reader import Reader
from services.plc_data_hub.src.utils import get_places_with_name_containing
from shared.logger import logger

logging.getLogger("app").setLevel(logging.WARNING)


async def initialize_readers():
    places = await get_places_with_name_containing("Кромочник")

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


if __name__ == "__main__":
    try:
        asyncio.run(initialize_readers())
    except Exception as e:
        logger.error(f"Ошибка при запуске приложения: {e}")
