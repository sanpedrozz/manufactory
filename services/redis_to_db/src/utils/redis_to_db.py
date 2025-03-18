import asyncio
from datetime import datetime

from shared.config import settings
from shared.db.manufactory.database import AsyncSessionFactory
from shared.db.manufactory.models import SensorHistory
from shared.logger import setup_logger
from shared.redis import RedisManager

log = setup_logger(__name__, 'INFO')


async def get_queues(redis_manager: RedisManager) -> list:
    """Получить список всех очередей, содержащих 'place' в их имени."""
    keys = redis_manager.get_all_keys()
    return [key for key in keys if "place" in key]


async def process_queue(queue_name: str, redis_manager: RedisManager):
    """Обработка всех очередей."""
    try:
        data_list = redis_manager.get_all_from_queue(queue_name)
        log.debug(f"Данные из очереди {queue_name}: {data_list}")
        if data_list:
            await save_to_db(data_list)
    except Exception as e:
        log.error(f"Ошибка обработки очереди {queue_name}: {e}")


async def save_to_db(data_list: list[dict]):
    """Записать данные в базу данных пачкой."""
    try:
        async with AsyncSessionFactory() as session:
            sensor_histories = []
            for data in data_list:
                if all(key in data for key in ["value", "place_id", "timestamp", "sensor_id"]):
                    sensor_histories.append(
                        SensorHistory(
                            value=str(data["value"]),
                            place_id=data["place_id"],
                            dt_created=datetime.fromisoformat(data["timestamp"]).replace(tzinfo=None),
                            sensor_id=data["sensor_id"]
                        )
                    )
                else:
                    log.error(f"Пропущены некорректные данные: {data}")

            if sensor_histories:
                session.add_all(sensor_histories)
                await session.commit()
            else:
                log.warning("Нет корректных данных для вставки в БД.")
    except Exception as e:
        log.error(f"Ошибка записи в БД: {e}")


async def process_redis_to_db():
    """
    Обработать все очереди, содержащие 'place' в их имени.
    """
    redis_manager = RedisManager(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT
    )
    log.info("Запущен процесс обработки данных из Redis.")

    while True:
        queues = await get_queues(redis_manager)
        if queues:
            tasks = [process_queue(queue_name, redis_manager) for queue_name in queues]
            await asyncio.gather(*tasks)
        else:
            log.debug("Очереди отсутствуют.")

        await asyncio.sleep(settings.REDIS_ASYNC_SLEEP_INTERVAL)
