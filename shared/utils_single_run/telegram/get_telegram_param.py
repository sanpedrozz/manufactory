import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message

from shared.config import settings

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


@dp.message()
async def get_ids(message: Message):
    chat_id = message.chat.id
    thread_id = message.message_thread_id  # Будет None, если сообщение не в топике

    if thread_id:
        response = (
            f"Chat ID (группа): {chat_id}\n"
            f"Message Thread ID (тема): {thread_id}"
        )
    else:
        response = f"Chat ID (группа): {chat_id}\nСообщение отправлено не в теме."

    await message.answer(response)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
