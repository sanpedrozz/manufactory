import asyncio

from aiogram import Bot, exceptions

from shared.config import settings

THREAD_IDS = []
MESSAGE_TEXT = "Это тестовое сообщение для всех тем!"


async def send_messages():
    bot = Bot(token=settings.BOT_TOKEN)
    for thread_id in THREAD_IDS:
        try:
            await bot.send_message(
                chat_id=settings.CHAT_ID,
                text=f"Сообщение для темы {thread_id}: {MESSAGE_TEXT}",
                message_thread_id=thread_id
            )
            print(f"✅ Сообщение успешно отправлено в тему {thread_id}")
        except exceptions.TelegramAPIError as e:
            print(f"❌ Ошибка при отправке в тему {thread_id}: {e}")

    await bot.close()


if __name__ == '__main__':
    asyncio.run(send_messages())
