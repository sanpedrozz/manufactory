from pydantic import BaseModel

from . import plc_models

#   Размер name и type
NAME_SIZE = 20
TYPE_SIZE = 30
ADD_STR_SIZE = 2
DB_SIZE = 2
BYTE_SIZE = 2
BIT_SIZE = 2

# Словарь для смещений данных
OFFSETS = {
    'name': 0,
    'type': NAME_SIZE + ADD_STR_SIZE,
    'db': TYPE_SIZE + NAME_SIZE + ADD_STR_SIZE * 2,
    'byte': TYPE_SIZE + NAME_SIZE + ADD_STR_SIZE * 2 + DB_SIZE,
    'bit': TYPE_SIZE + NAME_SIZE + ADD_STR_SIZE * 2 + DB_SIZE + BYTE_SIZE,
}

# Полный размер
FULL_SIZE = TYPE_SIZE + NAME_SIZE + ADD_STR_SIZE * 2 + DB_SIZE + BYTE_SIZE + BIT_SIZE


class PLCTag(BaseModel):
    name: str
    type: str
    db: int
    byte: int
    bit: int

    @classmethod
    def get_tag(cls, data: bytes, offset: int) -> "PLCTag":
        """
        Создает объект PLCTag на основе сырых данных и смещения.

        :param data: Сырые данные из PLC
        :param offset: Смещение, с которого начинаются данные
        :return: Объект PLCTag с извлеченными данными
        """
        return cls(
            name=plc_models['String[20]'].read_func(data, offset + OFFSETS['name']),
            type=plc_models['String[30]'].read_func(data, offset + OFFSETS['type']),
            db=plc_models['UInt'].read_func(data, offset + OFFSETS['db']),
            byte=plc_models['UInt'].read_func(data, offset + OFFSETS['byte']),
            bit=plc_models['USInt'].read_func(data, offset + OFFSETS['bit'])
        )
