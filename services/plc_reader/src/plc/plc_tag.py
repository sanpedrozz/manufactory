from pydantic import BaseModel
from . import models


class Tag(BaseModel):
    name: str
    type: str
    db: int
    byte: int
    bit: int

    @classmethod
    def from_data(cls, data: bytes, offset: int) -> "Parameter":
        """Метод для извлечения данных и создания объекта Parameter."""
        return cls(
            name=models['String[20]'].read_func(data, offset),
            type=models['String[30]'].read_func(data, offset + 22),
            db=models['UInt'].read_func(data, offset + 54),
            byte=models['UInt'].read_func(data, offset + 56),
            bit=models['USInt'].read_func(data, offset + 58)
        )
