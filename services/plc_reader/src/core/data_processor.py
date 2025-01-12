import logging
from datetime import datetime
from typing import List, Dict, Any, Callable

from services.plc_reader.src.core.sensor_cache import SensorCache
from shared.logger.logger import logger
from shared.redis import RedisManager


class DataProcessor:
    """Базовый класс для обработки данных."""

    def __init__(self, place_id: int, redis_host='redis', redis_port=6379, redis_db=0):
        self.place_id = place_id
        self.current_values: Dict[str, Any] = {}
        self.previous_values: Dict[str, Any] = {}
        self.sensor_cache = SensorCache()
        self.redis_manager = RedisManager(host=redis_host, port=redis_port, db=redis_db)
        self.queue_name = f"place_{self.place_id}_data"

        self.processors: Dict[str, Callable[[str, Any], Any]] = {
            "outDataNonVerify": self.process_out_data,
            "outDataVerify": self.process_out_data,
        }

        self.logger = logger.getChild("Reader")
        self.logger.setLevel(logging.INFO)

    def initialize(self) -> None:
        """Инициализирует кэш сенсоров."""
        self.sensor_cache.load_cache()

    def process_out_data(self, key: str, values: List[Any]) -> None:
        """Обработка данных для outDataNonVerify и outDataVerify."""
        prev_values = self.previous_values.get(key, [])
        new_values = [value for value in values if value not in prev_values]
        sensor_id = self.sensor_cache.get_or_create_sensor_id(key)
        for value in new_values:
            data = {
                "place_id": self.place_id,
                "sensor_id": sensor_id,
                "value": value,
                "timestamp": datetime.utcnow().isoformat(),
            }
            self.redis_manager.add_to_queue(self.queue_name, data)

    def process_default(self, key: str, value: Any) -> None:
        """Обработка данных по умолчанию для остальных ключей."""
        if self.previous_values.get(key) != value:
            self.sensor_cache.get_or_create_sensor_id(key)
            data = {
                "place_id": self.place_id,
                "key": key,
                "value": value,
                "timestamp": datetime.utcnow().isoformat(),
            }
            self.redis_manager.add_to_queue(self.queue_name, data)
