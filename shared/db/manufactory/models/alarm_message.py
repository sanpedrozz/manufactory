from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from shared.db.base import Base


class AlarmMessage(Base):
    __tablename__ = "alarm_message"

    id = Column(BigInteger, primary_key=True)
    message = Column(String(255), nullable=False)
    tag_id = Column(Integer, ForeignKey("alarms_tag.id", ondelete="SET NULL"), nullable=True)

    tag = relationship("AlarmTag", back_populates="alarm_message")
    alarm_history = relationship("AlarmHistory", back_populates="message", cascade="all, delete-orphan")
