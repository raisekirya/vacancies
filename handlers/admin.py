from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from outboxes.admin import AddManagerState

router = Router()

import outboxes.admin as outbox


@router.callback_query(F.data.startswith("admin:managers_page_"))
async def show_mangers(callback: CallbackQuery):
    await outbox.show_managers(callback)


@router.callback_query(F.data.startswith("admin:manager_"))
async def show_manager(callback: CallbackQuery):
    await outbox.show_manager(callback)


@router.callback_query(F.data == "admin:add_manager")
async def add_manager(callback: CallbackQuery, state: FSMContext):
    await outbox.add_manager(callback, state)


@router.message(F.text, StateFilter(AddManagerState.username))
async def process_add_manager(message: Message, state: FSMContext):
    await outbox.process_add_manager(message, state)


@router.callback_query(F.data.startswith("admin:delete_manager_"))
async def delete_manager(callback: CallbackQuery):
    await outbox.delete_manager(callback)


@router.callback_query(F.data == "admin:back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    await outbox.menu(callback.message)
