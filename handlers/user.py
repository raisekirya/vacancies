from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

import keyboards.user as kb
from config import ADMIN_CHAT_ID
from database.functions import get_user_by_tg_id, get_manager_by_id, create_user
from outboxes.admin import menu as admin_menu, ERROR_MESSAGE
from utils.appoint_manager import get_next_manager_id

router = Router()


class RegistrationState(StatesGroup):
    data = State()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    try:
        if message.from_user.id == ADMIN_CHAT_ID:
            await admin_menu(message)
            return

        user = await get_user_by_tg_id(message.from_user.id)

        if user:
            manager = await get_manager_by_id(user[2])

            await message.answer(
                f"✅ Вы уже зарегистрированы!\n\n"
                f"📍 Город: {str(user[3]).capitalize()}\n"
                f"📅 Возраст: {user[4]}\n"
                f"📱 Username: @{message.from_user.username}"
            )

            await message.answer(
                "📞 Для связи с менеджером используйте кнопку ниже:",
                reply_markup=kb.message_manager(manager[1])
            )

            return

        else:
            await message.answer(
                """Для связи с нашим менеджером заполните анкету по примеру:
                
                1. Ваш город
                2.Ваш возраст
                
                Например: Москва, 41"""
            )

            await state.set_state(RegistrationState.data)

    except Exception as e:
        print(f"Error: {str(e)}")
        await message.answer(ERROR_MESSAGE)


@router.message(F.text, StateFilter(RegistrationState.data))
async def register(message: Message, state: FSMContext):
    try:
        manager_id = await get_next_manager_id()
        manager = await get_manager_by_id(manager_id)

        await create_user(
            tg_id=message.from_user.id,
            manager_id=manager_id,
            city=message.text,  # Сохраняем весь текст как "город"
            age=0  # Устанавливаем возраст как 0 или любое дефолтное значение
        )

        await message.answer(
            "Спасибо , ваши данные отправлены ✅\n"
            "Напишите вашему менеджеру 📩"
        )

        await message.answer(
            "📞 Для связи с менеджером используйте кнопку ниже:",
            reply_markup=kb.message_manager(manager[1])
        )

        await state.clear()

    except Exception as e:
        print(f"Error: {str(e)}")
        await message.answer(ERROR_MESSAGE)

        await state.clear()
