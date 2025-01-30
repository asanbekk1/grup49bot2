import asyncio
import logging
from aiogram import Bot

from bot_config import bot, dp
from handlers.group_management import group_router


async def main():
    dp.include_router(group_router)

    # запуск бота
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())