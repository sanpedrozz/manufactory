from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from shared.db.manufactory.models import Sensor


class SensorCache:
    """Класс для кэширования данных из таблицы Sensor."""

    def __init__(self):
        self.cache: Dict[str, int] = {}

    async def load_cache(self, session: AsyncSession) -> None:
        """Загружает данные из таблицы Sensor в кэш."""
        result = await session.execute(select(Sensor))
        sensors = result.scalars().all()
        self.cache = {sensor.name: sensor.id for sensor in sensors}

    async def get_or_create_sensor_id(self, session: AsyncSession, name: str) -> int:
        """
        Возвращает ID сенсора из кэша или создает новую запись в таблице Sensor.
        :param session: Текущая сессия базы данных.
        :param name: Имя сенсора.
        :return: ID сенсора.
        """
        if name in self.cache:
            return self.cache[name]

        # Создаем новый сенсор в таблице
        new_sensor = Sensor(name=name)
        session.add(new_sensor)
        await session.flush()  # Генерирует ID для нового сенсора

        # Добавляем в кэш
        self.cache[name] = new_sensor.id
        return new_sensor.id
