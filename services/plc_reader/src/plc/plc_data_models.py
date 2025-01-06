from snap7.util import get_string, get_int, get_real, get_bool, get_dint, get_uint, get_usint


class DataType:
    """Базовый класс для типов данных ПЛК."""

    def __init__(self, name, size, read_func):
        self.name = name
        self._size = size
        self.read_func = read_func

    @property
    def size(self):
        """Возвращает размер типа данных в байтах."""
        return self._size


class IntDataType(DataType):
    """Целочисленный тип данных, использует get_int из snap7."""

    def __init__(self):
        super().__init__('Int', 2, get_int)


class RealDataType(DataType):
    """Тип данных Real (с плавающей точкой), использует get_real из snap7."""

    def __init__(self):
        super().__init__('Real', 4, get_real)


class BoolDataType(DataType):
    """Булевый тип данных, использует get_bool из snap7."""

    def __init__(self):
        super().__init__('Bool', 1, get_bool)


class UIntDataType(DataType):
    """Тип данных беззнаковое целое, использует get_uint из snap7."""

    def __init__(self):
        super().__init__('UInt', 2, get_uint)


class USIntDataType(DataType):
    """Тип данных беззнаковое малое целое, использует get_usint из snap7."""

    def __init__(self):
        super().__init__('USInt', 1, get_usint)


class DIntDataType(DataType):
    """Тип данных двойное целое, использует get_dint из snap7."""

    def __init__(self):
        super().__init__('DInt', 4, get_dint)


class StringDataType(DataType):
    """Тип данных String с определённым размером, использует get_string из snap7."""

    _cache = {}

    def __new__(cls, size=256):
        if size in cls._cache:
            return cls._cache[size]
        instance = super().__new__(cls)
        cls._cache[size] = instance
        return instance

    def __init__(self, size=256):
        if hasattr(self, '_initialized') and self._initialized:
            return
        super().__init__(f"String[{size}]", size + 2 if size <= 254 else size, get_string)
        self._initialized = True


class ArrayDataType(DataType):
    """Тип данных Array, представляющий массив из одинаковых элементов."""

    def __init__(self, base_type: DataType, start_index: int, end_index: int):
        self.base_type = base_type
        self.start_index = start_index
        self.end_index = end_index
        self.length = end_index - start_index + 1
        name = f"Array[{start_index}..{end_index}] of {base_type.name}"
        size = base_type.size * self.length
        super().__init__(name, size, self._read_array)

    def _read_array(self, buffer, offset=0):
        """Считывает массив из буфера и возвращает список элементов."""
        values = []
        for i in range(self.length):
            element_offset = offset + i * self.base_type.size
            value = self.base_type.read_func(buffer, element_offset)
            values.append(value)
        return values

    def get_element(self, buffer, index, offset=0):
        """Возвращает элемент массива по индексу."""
        if index < self.start_index or index > self.end_index:
            raise IndexError(f"Индекс {index} выходит за границы массива {self.start_index}..{self.end_index}.")
        element_offset = offset + (index - self.start_index) * self.base_type.size
        return self.base_type.read_func(buffer, element_offset)


models = {
    'Int': IntDataType(),
    'Real': RealDataType(),
    'Bool': BoolDataType(),
    'UInt': UIntDataType(),
    'USInt': USIntDataType(),
    'DInt': DIntDataType(),
    'String': StringDataType()
}

models.update({f'String[{i}]': StringDataType(i) for i in range(1, 255)})

for size in range(1, 255):
    models.update({
        f'Array[1..10] of String[{size}]': ArrayDataType(StringDataType(size), 1, 10)}
    )

if __name__ == '__main__':
    for key in models:
        print(f"{key}: {models[key].size} байт")
