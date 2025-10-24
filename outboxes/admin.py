from typing import Final

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

import keyboards.admin as kb
from database.functions import get_all_managers, create_manager, get_manager_by_id, delete_manager as db_delete_manager

ERROR_MESSAGE: Final = "❌ Произошла ошибка. Попробуйте позже."


class AddManagerState(StatesGroup):
    username = State()


async def menu(message: Message):
    await message.answer("👋 Вы находитесь в админ-панели.", reply_markup=kb.menu())


async def show_managers(callback: CallbackQuery):
    try:
        page = int(callback.data.split("_")[-1])
        managers = await get_all_managers()

        await callback.message.edit_text(
            "👥 Менеджеры",
            reply_markup=await kb.show_managers(managers, page)
        )

    except Exception as e:
        print(f"Error showing managers for admin: {str(e)}")
        await callback.message.answer(ERROR_MESSAGE, reply_markup=kb.back_to_menu())

    await callback.answer()


async def show_manager(callback: CallbackQuery):
    try:
        manager_id = int(callback.data.split("_")[-1])
        manager = await get_manager_by_id(manager_id)

        await callback.message.answer(
            f"👤 Менеджер №{manager[0]}\n"
            f"🪪 Username: @{manager[1]}",
            reply_markup=kb.show_manager(manager[0])
        )

    except Exception as e:
        print(f"Error showing manager for admin: {str(e)}")
        await callback.message.answer(ERROR_MESSAGE, reply_markup=kb.back_to_menu())

    await callback.answer()


async def add_manager(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.answer(
            "Пожалуйста, отправьте юзернейм нового менеджера.\n"
            "Пример: <code>@test_manager</code>.",
            reply_markup=kb.back_to_menu(),
            parse_mode="HTML"
        )

        await state.set_state(AddManagerState.username)

    except Exception as e:
        print(f"Error ask admin for new manager username to create him: {str(e)}")
        await callback.message.answer(ERROR_MESSAGE, reply_markup=kb.back_to_menu())
        await state.clear()

    await callback.answer()


async def process_add_manager(message: Message, state: FSMContext):
    try:
        username = message.text.replace("@", "")
        await create_manager(username)

        await message.answer("Новый менеджер успешно добавлен.", reply_markup=kb.back_to_menu())

        await state.clear()

    except Exception as e:
        print(f"Error creating new manager: {str(e)}")
        await message.answer(ERROR_MESSAGE, reply_markup=kb.back_to_menu())
        await state.clear()


async def delete_manager(callback: CallbackQuery):
    try:
        manager_id = int(callback.data.split("_")[-1])
        await db_delete_manager(manager_id)

        await callback.message.answer("Менеджер успешно удален.", reply_markup=kb.back_to_menu())

    except Exception as e:
        print(f"Error deleting manager: {str(e)}")
        await callback.message.answer(ERROR_MESSAGE, reply_markup=kb.back_to_menu())

    await callback.answer()
