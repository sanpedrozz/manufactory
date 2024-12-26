from sqlalchemy import Column, Text, BigInteger
from sqlalchemy.orm import relationship

from shared.db.base import Base


class AlarmMessages(Base):
    __tablename__ = "alarm_messages"
    id = Column(BigInteger, primary_key=True)
    message = Column(Text, nullable=True)
    tag = Column(Text, nullable=True)

    alarm_histories = relationship("AlarmHistory", back_populates="alarm", post_update=True)  # Добавлено
