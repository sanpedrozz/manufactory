import asyncio
from typing import List, Dict, Any

from services.plc_reader.src.plc import PLCClient, plc_models, PLCTag
from shared.config import settings
from shared.db.manufactory.models.place import Place
from shared.logger.logger import logger


class Reader:
    """Класс для взаимодействия с ПЛК, чтения данных из заданного DB и извлечения информации о типах данных."""

    def __init__(self, place: Place):
        self.place = place
        self.client = PLCClient(self.place.ip)
        self.tag_list: List[PLCTag] = []
        self.current_values: Dict[str, Any] = {}
        self.previous_values: Dict[str, Any] = {}

    async def _fetch_tags_count(self) -> int:
        """Чтение количества заполненных элементов массива из PLC."""
        data = self.client.read_data(db_number=settings.DB_NUMBER, offset=0, size=2)
        return plc_models['UInt'].read_func(data, 0)

    async def _fetch_tags(self, filled_array: int) -> List[PLCTag]:
        """Чтение данных массива из PLC и преобразование их в список объектов PLCTag."""
        return [
            PLCTag.get_tag(
                self.client.read_data(db_number=settings.DB_NUMBER, offset=2 + 60 * i, size=60),
                0
            )
            for i in range(filled_array)
        ]

    async def _read_plc_data(self) -> None:
        """Чтение данных из PLC и сохранение в текущих значениях."""
        self.current_values.clear()

        for tag in self.tag_list:
            model = plc_models.get(tag.type)
            if not model:
                logger.warning(f"Неизвестный тип данных {tag.type} для параметра {tag.name} (место: {self.place.name})")
                continue

            data = self.client.read_data(db_number=tag.db, offset=tag.byte, size=model.size)
            self.current_values[tag.name] = model.read_func(data, tag.bit)

    async def _save_plc_data(self):
        """Сохранение изменений в данные, если значения изменились."""
        for name, value in self.current_values.items():
            if isinstance(value, list):
                current_items = value
                previous_items = self.previous_values.get(name, [])

                # Сравниваем элементы списка
                for current_item in current_items:
                    if current_item not in previous_items:
                        new_data = {'place_id': self.place.id, 'value_name': name, 'value': current_item}
                        logger.info(f"{new_data}")

            elif self.previous_values.get(name) != value:
                new_data = {'place_id': self.place.id, 'value_name': name, 'value': value}

                logger.info(f"{new_data}")

        # Обновляем last_readings
        self.previous_values = self.current_values.copy()

    async def run(self) -> None:
        """Основной цикл чтения и обработки данных из PLC."""
        prev_tag_count = 0
        with self.client:
            while True:
                cur_tag_count = await self._fetch_tags_count()
                if cur_tag_count != prev_tag_count:
                    self.tag_list = await self._fetch_tags(cur_tag_count)
                    prev_tag_count = cur_tag_count
                    logger.info(f"Обновлено количество тегов: {prev_tag_count}")

                await self._read_plc_data()
                await self._save_plc_data()
                await asyncio.sleep(1)
