import asyncio
from datetime import datetime

from shared.config import settings
from shared.db.manufactory.database import AsyncSessionFactory
from shared.db.manufactory.models import SensorHistory
from shared.logger import logger
from shared.redis import RedisManager


async def get_queues(redis_manager: RedisManager) -> list:
    """Получить список всех очередей, содержащих 'place' в их имени."""
    keys = redis_manager.get_all_keys()
    return [key for key in keys if "place" in key]


async def process_queue(queue_name: str, redis_manager: RedisManager):
    """Обработка всех очередей."""
    try:
        data_list = redis_manager.get_all_from_queue(queue_name)
        if data_list:
            await save_to_db(data_list)
    except Exception as e:
        logger.error(f"Ошибка обработки очереди {queue_name}: {e}")


async def save_to_db(data_list: list[dict]):
    """Записать данные в базу данных пачкой."""
    try:
        async with AsyncSessionFactory() as session:
            sensor_histories = [
                SensorHistory(
                    value=str(data["value"]),
                    place_id=data["place_id"],
                    dt_created=datetime.fromisoformat(data["timestamp"]),
                    sensor_id=data["sensor_id"]
                )
                for data in data_list
            ]
            session.add_all(sensor_histories)
            await session.commit()
    except Exception as e:
        logger.error(f"Ошибка записи в БД: {e}")


async def process_redis_to_db():
    """
    Обработать все очереди, содержащие 'place' в их имени.
    """
    redis_manager = RedisManager(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT
    )
    logger.info("Запущен процесс обработки данных из Redis.")

    while True:
        queues = await get_queues(redis_manager)
        if queues:
            tasks = [process_queue(queue_name, redis_manager) for queue_name in queues]
            await asyncio.gather(*tasks)
        else:
            logger.debug("Очереди отсутствуют.")

        await asyncio.sleep(settings.REDIS_ASYNC_SLEEP_INTERVAL)
