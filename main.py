import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from database.database import create_tables
from handlers import routers

logging.basicConfig(
    level=logging.INFO
)


async def set_descriptions(bot: Bot):
    await bot.set_my_description("""
Что умеет этот бот ? Приветствуем вас🤝

Вы обратились в компанию по набору персонала в Норвегию 🇳🇴

💼 Большой выбор вакансий:

👷 Строители
🌿 Работники теплиц
🏨 Персонал отелей
🚚 Водители категории B
📦 Упаковщики на склад 
🔒 Разнорабочие
💶 Высокая оплата труда 

Для консультации с менеджером запустите бот по кнопке снизу👇 или нажмите /start
    """)

    await bot.set_my_short_description(
        "🇳🇴 Здесь вы найдете официальную работу в Норвегии. Большой выбор вакансий, жильё и питание включены"
    )


async def main():
    await create_tables()

    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    dp.include_routers(*routers)

    await set_descriptions(bot)
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
