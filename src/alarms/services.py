# src/alarms/services.py

from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from src.db.models import Place, PlaceCameraLink, AlarmMessages
from src.camera.services import get_video, dell_video
from src.alarms.schemas import Alarm
from src.bot.services import send_video, send_message


async def alarm_message(db: AsyncSession, alarm: Alarm):
    current_time = datetime.now()

    # Сборка данных для сообщения
    place = await Place.get_place_by_id(db, alarm.place_id)
    alarm_data = await AlarmMessages.get_alarm_by_id(db, alarm.alarm)

    # Сборка сообщения
    message = (f'Место аварии: {place.name}\n'
               f'Точное время: {current_time}\n'
               f'Авария: {alarm_data.message}\n'
               f'{alarm_data.tag}')

    # Выгрузка видео
    cameras_list = await Place.get_cameras_by_place_id(db, alarm.place_id)
    path_list = []
    for camera in cameras_list:
        path = await get_video(camera.camera_info, current_time)
        if path is not None:
            path_list.append(path)
        else:
            message = (f'{message}\n'
                       f'#ВИДЕО_НЕ_ПОЛУЧИЛОСЬ_ВЫГРУЗИТЬ_КАМЕРА_{camera.comment}')

    if path_list:
        await send_video(path_list, message, place.message_thread_id)
    else:
        await send_message(message, place.message_thread_id)

    for path in path_list:
        dell_video(path)


async def get_camera_info_by_place_id(db: AsyncSession, id: int):
    try:
        # Select the place and join the necessary relationships
        stmt = select(Place).options(
            joinedload(Place.camera_links).joinedload(PlaceCameraLink.camera)
        ).filter(Place.id == id)

        result = await db.execute(stmt)
        place = result.scalars().first()

        if not place:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Place with id {id} not found"
            )

        camera_info_list = [link.camera.camera_info for link in place.camera_links]
        return camera_info_list

    except SQLAlchemyError as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex)
        ) from ex
