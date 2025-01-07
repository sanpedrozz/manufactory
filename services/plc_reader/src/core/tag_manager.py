from typing import List

from services.plc_reader.src.plc import PLCTag, FULL_SIZE, PLCClient, plc_models
from shared.config import settings
from shared.logger.logger import logger


class TagManager:
    """Базовый класс для управления тегами."""

    def __init__(self, client: PLCClient):
        self.client = client
        self.db_number = settings.DB_NUMBER
        self.tag_list: List[PLCTag] = []

    def _fetch_tag_count(self) -> int:
        """Возвращает количество заполненных элементов массива тегов."""
        data = self.client.read_data(db_number=self.db_number, offset=0, size=2)
        return plc_models['UInt'].read_func(data, 0)

    def _fetch_tags(self, count: int) -> List[PLCTag]:
        """Читает массив тегов из PLC."""
        return [
            PLCTag.get_tag(
                self.client.read_data(db_number=self.db_number, offset=2 + FULL_SIZE * i, size=FULL_SIZE),
                0
            )
            for i in range(count)
        ]

    def update_tags(self, prev_tag_count: int) -> int:
        """
        Обновляет список тегов, если количество изменилось.
        :param prev_tag_count: Предыдущее количество тегов.
        :return: Новое количество тегов.
        """
        cur_tag_count = self._fetch_tag_count()
        if cur_tag_count != prev_tag_count:
            self.tag_list = self._fetch_tags(cur_tag_count)
            logger.info(f"Обновлено количество тегов: {cur_tag_count}")
        return cur_tag_count
