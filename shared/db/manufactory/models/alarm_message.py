from sqlalchemy import BigInteger, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from shared.db.base import Base


class AlarmMessage(Base):
    __tablename__ = "alarm_message"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    message = Column(String(255), nullable=False, unique=True)
    tag_id = Column(BigInteger, ForeignKey("alarm_tag.id", ondelete="SET NULL"), nullable=True)

    tag = relationship("AlarmTag", back_populates="alarm_messages")
    alarm_histories = relationship("AlarmHistory", back_populates="message", cascade="all, delete-orphan")
