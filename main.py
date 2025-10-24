import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from database.database import create_tables
from handlers import routers

logging.basicConfig(
    level=logging.INFO
)


async def main():
    await create_tables()

    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    dp.include_routers(*routers)

    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())
