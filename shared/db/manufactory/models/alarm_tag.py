from sqlalchemy import BigInteger, Column, String
from sqlalchemy.orm import relationship

from shared.db.base import Base


class AlarmTag(Base):
    __tablename__ = "alarm_tag"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tag = Column(String(100), nullable=False)

    alarm_message = relationship("AlarmMessage", back_populates="tag", cascade="all, delete-orphan")
