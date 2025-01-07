from datetime import datetime
from typing import List, Dict, Any, Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.plc_reader.src.core.sensor_cache import SensorCache
from shared.db.manufactory.database import AsyncSessionFactory
from shared.db.manufactory.models import SensorHistory


class DataProcessor:
    """Базовый класс для обработки данных."""

    def __init__(self, place_id: int):
        self.place_id = place_id
        self.current_values: Dict[str, Any] = {}
        self.previous_values: Dict[str, Any] = {}
        self.sensor_cache = SensorCache()

        self.processors: Dict[str, Callable[[str, Any], Any]] = {
            "outDataNonVerify": self.process_out_data,
            "outDataVerify": self.process_out_data,
        }

    async def initialize(self) -> None:
        """Инициализирует кэш сенсоров."""
        async with AsyncSessionFactory() as session:
            await self.sensor_cache.load_cache(session)

    async def process_out_data(self, key: str, values: List[Any]) -> None:
        """Асинхронная обработка данных для outDataNonVerify и outDataVerify."""
        async with AsyncSessionFactory() as session:
            prev_values = self.previous_values.get(key, [])
            new_values = [value for value in values if value not in prev_values]
            for value in new_values:
                sensor_id = await self.sensor_cache.get_or_create_sensor_id(session, key)
                await self.save_sensor_history(session, sensor_id, value)

    async def process_default(self, key: str, value: Any) -> None:
        """Асинхронная обработка данных по умолчанию для остальных ключей."""
        async with AsyncSessionFactory() as session:
            if self.previous_values.get(key) != value:
                sensor_id = await self.sensor_cache.get_or_create_sensor_id(session, key)
                await self.save_sensor_history(session, sensor_id, value)

    async def save_sensor_history(self, session: AsyncSession, sensor_id: int, value: Any) -> None:
        """Сохраняет запись в sensor_history, если такой записи еще нет."""
        # Проверяем наличие записи
        existing_entry = await session.execute(
            select(SensorHistory).where(
                SensorHistory.sensor_id == sensor_id,
                SensorHistory.place_id == self.place_id,
                SensorHistory.value == str(value)
            )
        )
        if existing_entry.scalars().first():
            # Запись уже существует
            return

        # Добавляем новую запись
        new_history = SensorHistory(
            value=str(value),
            dt_created=datetime.utcnow(),
            place_id=self.place_id,
            sensor_id=sensor_id,
        )
        session.add(new_history)
        await session.commit()
