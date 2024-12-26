from aiogram import Bot

from shared.config.config import settings

bot = Bot(token=settings.BOT_TOKEN)


async def send_message(message: str, message_thread_id: str = None):
    try:
        await bot.send_message(chat_id=settings.CHAT_ID, message_thread_id=message_thread_id, text=message)
    except Exception as e:
        error_message = f"Сообщение отправить не получилось: {e}"
        await bot.send_message(chat_id=settings.CHAT_ID, message_thread_id=message_thread_id, text=error_message)
    finally:
        await bot.session.close()
