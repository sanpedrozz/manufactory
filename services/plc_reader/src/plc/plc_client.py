import logging
from functools import wraps
from time import sleep

from snap7 import client

from shared.logger.logger import logger

logging.getLogger("snap7").setLevel(logging.CRITICAL)


def reconnect_on_fail(delay=5):
    """
    Декоратор, обеспечивающий повторное подключение к контроллеру PLC при сбоях соединения.
    :param delay: Задержка (в секундах) между попытками переподключения
    :return: Декорированная функция
    """

    def decorator(function):
        @wraps(function)
        def wrapper(self, *args, **kwargs):
            while True:
                try:
                    if self.connected:
                        return function(self, *args, **kwargs)
                    self.connect()
                except Exception as error:
                    logger.warning(f'PLC error for {self.ip}: {error}')
                    self.disconnect()
                    sleep(delay)

        return wrapper

    return decorator


class PLCClient:
    def __init__(self, ip: str):
        self.ip = ip
        self.client = client.Client()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    @property
    def connected(self):
        """
        Проверяет, установлено ли соединение с контроллером PLC
        :return: True, если соединение установлено, иначе False
        """
        return self.client.get_connected()

    def connect(self):
        """
        Устанавливает соединение с контроллером PLC.
        """
        if not self.connected:
            self.client.connect(self.ip, 0, 1)
            logger.info(f'Connected to PLC at {self.ip}')

    def disconnect(self):
        """
        Разрывает соединение с контроллером PLC.
        """
        if self.connected:
            self.client.disconnect()
            logger.info(f'Disconnected from PLC at {self.ip}')

    @reconnect_on_fail()
    def read_data(self, db_number: int, offset: int, size: int):
        """
        Читает данные из указанной области данных (DB) контроллера PLC.
        :param db_number: Int - Номер области данных (DB).
        :param offset: Int - Смещение начального байта в области данных.
        :param size: Int - Размер читаемых данных (в байтах).
        :return: Прочитанные данные.
        """
        return self.client.db_read(db_number, offset, size)

    @reconnect_on_fail()
    def write_data(self, db_number: int, start: int, data: bytearray):
        """
        Записывает данные в указанную область данных (DB) контроллера PLC
        :param db_number: Int - Номер области данных (DB).
        :param start: Int - Смещение начального байта в области данных.
        :param data: Int - Размер читаемых данных (в байтах).
        :return: Результат операции записи (количество записанных байт).
        """
        return self.client.db_write(db_number, start, data)
