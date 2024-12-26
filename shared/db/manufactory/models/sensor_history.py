from datetime import datetime

from sqlalchemy import Column, BigInteger, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from shared.db.base import Base


class SensorHistory(Base):
    __tablename__ = "sensor_history"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    value = Column(Text, nullable=False)
    dt_created = Column(DateTime, default=datetime.utcnow, nullable=False)
    place_id = Column(BigInteger, ForeignKey("place.id", ondelete="CASCADE"), nullable=False)
    sensor_id = Column(BigInteger, ForeignKey("sensor.id", ondelete="CASCADE"), nullable=False)

    place = relationship("Place", back_populates="sensor_histories")
    sensor = relationship("Sensor", back_populates="sensor_histories")
