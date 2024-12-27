from sqlalchemy.future import select

from services.alarm.src.models import Alarm
from shared.db.manufactory.database import AsyncSessionFactory
from shared.db.manufactory.models import Place, AlarmMessage, AlarmTag, AlarmHistory
from shared.telegram import send_message


async def send_alarm_to_telegram(alarm: Alarm, dt):
    async with AsyncSessionFactory() as session:
        alarm_id = alarm.alarm
        place_id = alarm.place_id

        stmt = (
            select(Place, AlarmMessage, AlarmTag)
            .select_from(Place)
            .join(AlarmMessage, alarm_id == AlarmMessage.id)
            .join(AlarmTag, AlarmTag.id == AlarmMessage.tag_id, isouter=True)
            .where(place_id == Place.id)
        )
        result = await session.execute(stmt)
        place, alarm_text, alarm_tag = result.first()

    message = (
        f"📍 {place.name}\n"
        f"🚨 {alarm_text.message}\n"
        f"⏰ {dt.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"📝 {alarm.comment}\n"
        f"{alarm_tag.tag}"
    )

    await send_message(message, place.message_thread_id)


async def add_alarm_to_db(alarm: Alarm, dt):
    async with AsyncSessionFactory() as session:
        async with session.begin():
            alarm_history = AlarmHistory(
                place_id=alarm.place_id,
                message_id=alarm.alarm,
                additional_data=alarm.comment if alarm.comment else "",
                dt_created=dt
            )
            await alarm_history.add(session)
