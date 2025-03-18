from typing import Dict

from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from shared.db.manufactory.database import SyncSessionFactory
from shared.db.manufactory.models import Sensor
from shared.logger import setup_logger

log = setup_logger(__name__, 'INFO')


class SensorCache:
    """Класс для кэширования данных из таблицы Sensor."""

    def __init__(self):
        self.cache: Dict[str, int] = {}

    def load_cache(self) -> None:
        """Загружает данные из таблицы Sensor в кэш."""
        with SyncSessionFactory() as session:
            result = session.execute(select(Sensor))
            sensors = result.scalars().all()
            self.cache = {sensor.name: sensor.id for sensor in sensors}

    def get_or_create_sensor_id(self, name: str) -> int:
        """
        Возвращает ID сенсора из кэша или создает новую запись в таблице Sensor.
        :param name: Имя сенсора.
        :return: ID сенсора.
        """
        if name in self.cache:
            return self.cache[name]

        # Пытаемся создать новый сенсор
        with SyncSessionFactory() as session:
            new_sensor = Sensor(name=name)
            session.add(new_sensor)
            try:
                session.flush()  # Генерирует ID для нового сенсора
                session.commit()  # Фиксация изменений
                self.cache[name] = new_sensor.id  # Добавляем в кэш
                return new_sensor.id
            except IntegrityError as e:
                log.error(f"IntegrityError occurred: {e}")
                session.rollback()
                # Если запись уже существует, загружаем ее ID
                existing_sensor = session.execute(select(Sensor).where(name == Sensor.name))
                sensor = existing_sensor.scalars().first()
                if sensor:
                    self.cache[name] = sensor.id  # Добавляем в кэш
                    return sensor.id
                raise
