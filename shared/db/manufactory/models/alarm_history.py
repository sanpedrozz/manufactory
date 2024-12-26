from datetime import datetime

from sqlalchemy import Column, ForeignKey, Text, BigInteger, DateTime
from sqlalchemy.orm import relationship

from shared.db.base import Base


class AlarmHistory(Base):
    __tablename__ = "alarm_history"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    place_id = Column(BigInteger, ForeignKey('places.id'), nullable=False)
    alarm_id = Column(BigInteger, ForeignKey('alarm_messages.id'), nullable=False)
    comments = Column(Text, nullable=True)
    dt_created = Column(DateTime, default=datetime.now, nullable=False)

    place = relationship("Place", back_populates="alarm_histories")
    alarm = relationship("AlarmMessages", back_populates="alarm_histories")
