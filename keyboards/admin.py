import math
from sqlite3 import Row
from typing import Iterable

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardBuilder


def menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="👥 Менеджеры", callback_data="admin:managers_page_1")
    builder.button(text="➕ Добавить менеджера", callback_data="admin:add_manager")

    builder.adjust(1)

    return builder.as_markup()


async def show_managers(managers: Iterable[Row], page: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    managers = list(managers)
    total_count = len(managers)
    total_pages = math.ceil(total_count / 8)

    start_index = (page - 1) * 8
    end_index = start_index + 8
    page_managers = managers[start_index:end_index]

    for manager in page_managers:
        manager_id, username = manager
        builder.row(
            InlineKeyboardButton(
                text=f"№{manager_id} | @{username}",
                callback_data=f"admin:manager_{manager_id}"
            )
        )

    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"admin:managers_page_{page - 1}"))
    if page < total_pages:
        nav_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"admin:managers_page_{page + 1}"))
    if nav_buttons:
        builder.row(*nav_buttons)

    builder.row(InlineKeyboardButton(text="↩️ Вернуться в меню", callback_data="admin:back_to_menu"))

    return builder.as_markup()


def show_manager(manager_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="❌ Удалить менеджера", callback_data=f"admin:delete_manager_{manager_id}")
    builder.button(text="↩️ Вернуться назад", callback_data="admin:managers_page_1")

    builder.adjust(1)

    return builder.as_markup()


def back_to_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="↩️ Вернуться в меню", callback_data="admin:back_to_menu")

    return builder.as_markup()
