import asyncio

from services.plc_data_hub.src.plc import PLCClient, models
from shared.config import settings
from shared.logger.logger import logger


class Reader:
    """Класс для взаимодействия с ПЛК, чтения данных из заданного DB и извлечения информации о типах данных."""

    def __init__(self, ip: str):
        self.client = PLCClient(ip)
        self.parameter_list = []
        self.parameter_count = 0
        self.current_values = {}
        self.previous_values = {}
        self.previous_parameter_count = None
        self.current_parameter_count = None

    async def _fetch_parameters_count(self) -> int:
        """
        Чтение количества заполненных элементов массива из PLC.
        :return: Количество заполненных элементов.
        """
        data = self.client.read_data(db_number=settings.DB_NUMBER, offset=0, size=2)
        return models['UInt'].read_func(data, 0)

    async def _fetch_parameters(self, filled_array):
        """
        Чтение данных массива из PLC и преобразует их в список словарей.
        :param filled_array: Количество элементов, которые нужно прочитать.
        :return: Список словарей с информацией о каждом элементе массива.
        """
        data_list = []
        # Чтение всех данных одним запросом, если возможно
        for i in range(filled_array):
            data = self.client.read_data(db_number=settings.DB_NUMBER, offset=2 + 60 * i, size=60)
            data_dict = {
                'name': models['String[20]'].read_func(data, 0),
                'type': models['String[30]'].read_func(data, 22),
                'db': models['UInt'].read_func(data, 54),
                'byte': models['UInt'].read_func(data, 56),
                'bit': models['USInt'].read_func(data, 58)
            }
            data_list.append(data_dict)
        return data_list

    async def _fetch_plc_data(self):
        """
        Чтение данных из другого DB на основе информации из data_buffer.
        :return: Список словарей со значениями в формате {name: value}.
        """
        self.current_values.clear()  # Очищаем предыдущие значения
        for entry in self.parameter_list:
            name = entry['name']
            db_number = entry['db']
            byte_offset = entry['byte']
            bit_offset = entry['bit']
            data_type = entry['type']

            # Определяем модель на основе типа данных
            model = models.get(data_type)
            if model:
                # Читаем данные из указанного DB, используя смещение в байтах и бите
                data = self.client.read_data(db_number=db_number, offset=byte_offset, size=model.size)

                # Разбираем прочитанные данные
                self.current_values[name] = model.read_func(data, bit_offset)
            else:
                logger.warning(f"Неизвестный тип данных: {data_type} для параметра {entry['name']}")

    async def run(self):
        """
        Основной цикл чтения данных из PLC.
        """
        with self.client:

            while True:
                self.current_parameter_count = await self._fetch_parameters_count()
                if self.current_parameter_count != self.previous_parameter_count:
                    self.parameter_list = await self._fetch_parameters(self.current_parameter_count)
                    self.previous_parameter_count = self.current_parameter_count

                await self._fetch_plc_data()
                await asyncio.sleep(0.1)
