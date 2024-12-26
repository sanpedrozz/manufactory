from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import relationship

from shared.db.base import Base


class Sensor(Base):
    __tablename__ = "sensor"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)

    sensor_histories = relationship("SensorHistory", back_populates="sensor", cascade="all, delete-orphan")
