from sqlalchemy import Column, Text, BigInteger
from sqlalchemy.orm import relationship

from shared.db.base import Base


class Sensor(Base):
    """
    Модель сенсора.
    """
    __tablename__ = "sensors"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    description = Column(Text)

    statistics = relationship("Statistics", back_populates="sensor")
