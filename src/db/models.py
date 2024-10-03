# src/db/models.py

from sqlalchemy import Column, ForeignKey, Text, Integer, BigInteger, DateTime, JSON, Boolean, String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from sqlalchemy.future import select
from fastapi import HTTPException, status
from typing import List, Dict
from datetime import datetime

from src.db.base import Base


class OperationHistory(Base):
    __tablename__ = "operations_history"
    id = Column(BigInteger, primary_key=True)
    place_id = Column(Integer, ForeignKey('places.id'))
    program = Column(Text)
    text = Column(Text)
    dt_created = Column(DateTime, default=datetime.now)

    place = relationship("Place", back_populates="operations")

    @classmethod
    async def get_all(cls, db: AsyncSession) -> List["OperationHistory"]:
        """
        Get all OperationHistory records.
        :param db: The database session.
        :return: A list of all OperationHistory records.
        """
        try:
            stmt = select(cls)
            result = await db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ex)
            ) from ex


class Place(Base):
    __tablename__ = "places"
    id = Column(BigInteger, primary_key=True)
    name = Column(Text)
    message_thread_id = Column(String, default="General", nullable=False)

    operations = relationship("OperationHistory", back_populates="place", post_update=True)

    @classmethod
    async def get_all(cls, db: AsyncSession) -> List["Place"]:
        """
        Get all Place records.
        :param db: The database session.
        :return: A list of all Place records.
        """
        try:
            stmt = select(cls)
            result = await db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ex)
            ) from ex

    @classmethod
    async def get_place_by_id(cls, db: AsyncSession, place_id: int) -> 'Place':
        """
        Get a Place record by ID.
        :param db: The database session.
        :param place_id: The place ID.
        :return: The Place record.
        """
        try:
            stmt = select(cls).filter(cls.id == place_id)
            result = await db.execute(stmt)
            place = result.scalars().first()

            if not place:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Place with id {place_id} not found"
                )

            return place
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(ex)
            ) from ex


class AlarmMessages(Base):
    __tablename__ = "alarm_messages"
    id = Column(BigInteger, primary_key=True)
    message = Column(Text, nullable=True)
    tag = Column(Text, nullable=True)

    @classmethod
    async def get_all(cls, db: AsyncSession) -> List["AlarmMessages"]:
        """
        Get all AlarmMessages records.
        :param db: The database session.
        :return: A list of all AlarmMessages records.
        """
        try:
            stmt = select(cls)
            result = await db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ex)
            ) from ex

    @classmethod
    async def get_alarm_by_id(cls, db: AsyncSession, alarm_id: int) -> 'AlarmMessages':
        """
        Get an AlarmMessages record by ID.
        :param db: The database session.
        :param alarm_id: The alarm ID.
        :return: The AlarmMessages record.
        """
        try:
            stmt = select(cls).filter(cls.id == alarm_id)
            result = await db.execute(stmt)
            alarm = result.scalars().first()

            if not alarm:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Alarm with id {alarm_id} not found"
                )

            return alarm
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(ex)
            ) from ex
