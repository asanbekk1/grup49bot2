import asyncio
import logging

from bot_config import bot, dp
from handlers.group_management import group_router
from handlers.homeworks import homework_router
from handlers.start import start_router


async def main():
    # dp.include_router(group_router)
    dp.include_router(start_router)
    dp.include_router(homework_router)

    # запуск бота
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())