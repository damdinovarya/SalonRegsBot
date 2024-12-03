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


def client_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Мои заявки", callback_data="client_show_claims"))
    builder.row(types.InlineKeyboardButton(text="Профиль", callback_data="client_show_profile"))
    builder.row(types.InlineKeyboardButton(text="Услуги", callback_data="client_show_services"))
    return builder


def client_profile_edit_keyboard(name, tel):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"{name}", callback_data="client_profile_edit_name"),
                types.InlineKeyboardButton(text=f"{tel}", callback_data="client_profile_edit_tel"))
    builder.row(types.InlineKeyboardButton(text=f"« Назад", callback_data="show_menu"))
    return builder
