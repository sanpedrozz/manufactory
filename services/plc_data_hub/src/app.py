import asyncio
import logging

from services.plc_data_hub.src.utils.utils import fetch_places
from services.plc_data_hub.src.core.plc_reader import Reader
from shared.db.manufactory.database import AsyncSessionFactory
from shared.logger import logger

logging.getLogger("main").setLevel(logging.WARNING)


async def initialize_readers():
    async with AsyncSessionFactory() as session:  # Создаём реальную сессию базы данных
        places = await fetch_places()  # Получаем список PLC

        if not places:
            logger.info("Нет подходящих PLC для подключения.")
            return

        tasks = []
        for place in places:
            logger.info(f"Инициализация Reader для {place.name} ({place.ip})")

            # Передаём реальную сессию
            async with AsyncSessionFactory() as place_session:
                reader = Reader(ip=place.ip, db_session=place_session)
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
