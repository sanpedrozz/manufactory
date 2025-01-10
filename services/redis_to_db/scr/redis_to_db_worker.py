import asyncio
from datetime import datetime

from shared.db.manufactory.database import get_async_db
from shared.redis import RedisManager


async def process_redis_to_db(queue_name: str):
    redis_manager = RedisManager()
    while True:
        data = redis_manager.get_from_queue(queue_name)
        if not data:
            continue

        await save_to_db(data)
        await asyncio.sleep(1)


async def save_to_db(data: dict):
    """Записать данные в базу данных."""
    async with get_async_db() as session:
        from shared.db.manufactory.models import SensorHistory
        sensor_history = SensorHistory(
            value=str(data["value"]),
            place_id=data["place_id"],
            dt_created=datetime.utcnow(),
            sensor_id=data.get("sensor_id", 0),  # Пример
        )
        session.add(sensor_history)
        await session.commit()
