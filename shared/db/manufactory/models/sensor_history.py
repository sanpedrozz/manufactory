from datetime import datetime

from sqlalchemy import Column, Text, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from shared.db.base import Base


class SensorHistory(Base):
    """
    Модель статистики с колонками place и sensor.
    """
    __tablename__ = "sensor_history"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    value = Column(Text, nullable=False)
    dt_created = Column(DateTime, default=datetime.now, nullable=False)
    place_id = Column(BigInteger, ForeignKey("places.id"), nullable=False)
    sensor_id = Column(BigInteger, ForeignKey("sensors.id"), nullable=False)

    place = relationship("Place", back_populates="statistics")
    sensor = relationship("Sensor", back_populates="statistics")
