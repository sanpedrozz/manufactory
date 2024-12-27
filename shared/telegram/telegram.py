from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from shared.config.config import settings
from shared.logger.logger import logger

bot = Bot(token=settings.BOT_TOKEN)


async def send_message(message: str, message_thread_id: str = None):
    """
    Отправляет сообщение в указанный чат.
    :param message: Сообщение.
    :param message_thread_id: ID потока в чате (опционально).
    """
    try:
        await bot.send_message(
            chat_id=settings.CHAT_ID,
            message_thread_id=message_thread_id,
            text=message
        )
        logger.info(f"Сообщение отправлено: {message}")
    except TelegramAPIError as e:
        logger.error(f"Ошибка Telegram API: {e}")
    except Exception as e:
        logger.exception(f"Непредвиденная ошибка при отправке сообщения: {e}")
    finally:
        await bot.session.close()
