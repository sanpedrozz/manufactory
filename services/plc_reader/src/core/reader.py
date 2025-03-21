import asyncio

from services.plc_reader.src.core.data_processor import DataProcessor
from services.plc_reader.src.core.tag_manager import TagManager
from services.plc_reader.src.plc import PLCClient, plc_models
from shared.db.manufactory.models.place import Place
from shared.logger import setup_logger

log = setup_logger(__name__, 'INFO')


class Reader(TagManager, DataProcessor):
    """Класс для взаимодействия с ПЛК, чтения данных из заданного DB и извлечения информации о типах данных."""

    def __init__(self, place: Place):
        #  TODO: Изменить модель, чтобы модель принималась из не бд, а своя модель
        TagManager.__init__(self, PLCClient(place.ip, place.name))
        DataProcessor.__init__(self, place.id)
        self.place = place

    def _read_plc_data(self) -> None:
        """Чтение данных из PLC и сохранение в текущих значениях."""
        self.current_values.clear()

        for tag in self.tag_list:
            model = plc_models.get(tag.type)
            if not model:
                log.warning(
                    f"Неизвестный тип данных {tag.type} для параметра {tag.name} (место: {self.place.name})")
                continue

            try:
                data = self.client.read_data(db_number=tag.db, offset=tag.byte, size=model.size)
                if tag.type == "Bool":
                    self.current_values[tag.name] = model.read_func(data, 0, tag.bit)
                else:
                    self.current_values[tag.name] = model.read_func(data, 0)
            except Exception as e:
                log.error(f"Ошибка чтения данных в {self.place.name} для тега {tag.name}: {e}")

    def _process_plc_data(self) -> None:
        """Сохранение изменений в данные, если значения изменились."""
        for key, value in self.current_values.items():
            processor = self.processors.get(key, self.process_default)
            try:
                processor(key, value)
            except Exception as e:
                log.error(f"Ошибка обработки данных в {self.place.name} для ключа {key}: {e}")

        self.previous_values = self.current_values.copy()

    async def run(self) -> None:
        """Основной цикл чтения и обработки данных из PLC."""
        prev_tag_count = 0

        with self.client:
            while True:
                try:
                    # Обновляем теги, если их количество изменилось
                    prev_tag_count = self.update_tags(prev_tag_count)

                    # Чтение данных из PLC
                    self._read_plc_data()

                    # Обработка данных
                    self._process_plc_data()

                except Exception as e:
                    log.error(f"Ошибка в основном цикле Reader: {e}")

                # Задержка перед следующим циклом
                await asyncio.sleep(0.1)
