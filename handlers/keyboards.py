from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from database import db


def get_client_tel_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Сохранить", callback_data="client_data_save"),
                types.InlineKeyboardButton(text="Редактировать", callback_data="client_data_edit"),
                width=2)
    return builder


def client_data_edit_keyboard(name, tel):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"{name}", callback_data="client_data_edit_name"),
                types.InlineKeyboardButton(text=f"{tel}", callback_data="client_data_edit_tel"),
                types.InlineKeyboardButton(text=f"« Назад", callback_data="user_await"),
                width=2)
    return builder
