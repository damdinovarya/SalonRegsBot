from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from database import db


def get_client_tel_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Сохранить", callback_data="client_data_save"),
                types.InlineKeyboardButton(text="Редактировать", callback_data="client_data_edit"),
                width=1)
    return builder


def client_data_edit_keyboard(name, tel):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"{name}", callback_data="client_data_edit_name"),
                types.InlineKeyboardButton(text=f"{tel}", callback_data="client_data_edit_tel"),
                width=1)
    return builder


def client_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Услуги", callback_data="client_show_services"))
    builder.row(types.InlineKeyboardButton(text="Мои заявки", callback_data="client_show_claims"))
    builder.row(types.InlineKeyboardButton(text="Профиль", callback_data="client_show_profile"))
    return builder


def client_show_profile_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Редактировать", callback_data="client_data_edit"),
                types.InlineKeyboardButton(text="« Назад", callback_data="start"),
                width=1)
    return builder