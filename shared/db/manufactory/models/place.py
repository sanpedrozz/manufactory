from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import relationship

from shared.db.base import Base


class Place(Base):
    __tablename__ = "place"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    message_thread_id = Column(String(100), default="General", nullable=False)
    ip = Column(String(39), nullable=True)

    operations = relationship("OperationHistory", back_populates="place", cascade="all, delete-orphan")
    alarm_histories = relationship("AlarmHistory", back_populates="place", cascade="all, delete-orphan")
