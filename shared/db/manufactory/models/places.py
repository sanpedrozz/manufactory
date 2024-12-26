from sqlalchemy import Column, Text, BigInteger, String
from sqlalchemy.orm import relationship

from shared.db.base import Base


class Place(Base):
    __tablename__ = "places"
    id = Column(BigInteger, primary_key=True)
    name = Column(Text)
    message_thread_id = Column(String, default="General", nullable=False)
    ip = Column(String(45), nullable=True)

    operations = relationship("OperationHistory", back_populates="place", post_update=True)
    alarm_histories = relationship("AlarmHistory", back_populates="place", post_update=True)
