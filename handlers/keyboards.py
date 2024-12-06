from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from database import db
from utils import rus_to_eng, eng_to_rus


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


def client_show_services_keyboard(client_services_titles):
    builder = InlineKeyboardBuilder()
    for service in client_services_titles:
        builder.row(
            types.InlineKeyboardButton(text=f"{service.capitalize()}", callback_data=f"client_show_services_{rus_to_eng(service)}"),
            width=1)
    builder.row(types.InlineKeyboardButton(text="« Назад", callback_data="start"),
                width=1)
    return builder


def client_show_workers_keyboard(workers, title):
    builder = InlineKeyboardBuilder()
    for worker in workers:
        builder.row(
            types.InlineKeyboardButton(text=f"{worker['name']} ({worker['rating']}⭐️)", callback_data=f"client_show_workers_{rus_to_eng(title)}_{worker['id']}"),
            width=1)
    builder.row(types.InlineKeyboardButton(text="« Назад", callback_data=f"client_show_services"),
                width=1)
    return builder
