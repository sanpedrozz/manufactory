from datetime import datetime

from sqlalchemy import Column, ForeignKey, BigInteger, DateTime, String
from sqlalchemy.orm import relationship

from shared.db.base import Base


class AlarmHistory(Base):
    __tablename__ = "alarm_history"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    place_id = Column(BigInteger, ForeignKey("places.id", ondelete="CASCADE"), nullable=False)
    message_id = Column(BigInteger, ForeignKey("alarm_message.id", ondelete="SET NULL"), nullable=False)
    additional_data = Column(String(200), nullable=True)
    dt_created = Column(DateTime, default=datetime.now, nullable=False)

    place = relationship("Place", back_populates="alarm_history")
    message = relationship("AlarmMessage", back_populates="alarm_history")
