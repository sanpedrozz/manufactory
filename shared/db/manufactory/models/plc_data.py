from datetime import datetime

from sqlalchemy import Column, Text, BigInteger, DateTime, String

from shared.db.base import Base


class PLCData(Base):
    __tablename__ = "plc_data"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    dt_created = Column(DateTime, default=datetime.now, nullable=False)
    name = Column(String, nullable=False)
    value = Column(Text, nullable=False)
