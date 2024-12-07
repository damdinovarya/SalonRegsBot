from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from database import db
from datetime import datetime, time
from utils import rus_to_eng, eng_to_rus


def get_client_tel_keyboard():
    """
    Создает клавиатуру с кнопками для сохранения или редактирования номера телефона пользователя.
    :return: InlineKeyboardBuilder объект с кнопками.
    """
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Сохранить", callback_data="client_data_save"),
                types.InlineKeyboardButton(text="Редактировать", callback_data="client_data_edit"),
                width=1)
    return builder


def client_data_edit_keyboard(name, tel):
    """
    Создает клавиатуру для перехода к редактированаю имени или телефона пользователя.
    :param name: Имя пользователя.
    :param tel: Телефон пользователя.
    :return: InlineKeyboardBuilder объект с кнопками.
    """
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"{name}", callback_data="client_data_edit_name"),
                types.InlineKeyboardButton(text=f"{tel}", callback_data="client_data_edit_tel"),
                width=1)
    return builder


def client_menu_keyboard():
    """
    Создает клавиатуру главного меню пользователя.
    :return: InlineKeyboardBuilder объект с кнопками.
    """
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Услуги", callback_data="client_show_services"))
    builder.row(types.InlineKeyboardButton(text="Мои заявки", callback_data="client_show_claims"))
    builder.row(types.InlineKeyboardButton(text="Профиль", callback_data="client_show_profile"))
    return builder


def client_show_profile_keyboard():
    """
    Создает клавиатуру для профиля пользователя с кнопками редактирования и возврата.
    :return: InlineKeyboardBuilder объект с кнопками.
    """
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Редактировать", callback_data="client_data_edit"),
                types.InlineKeyboardButton(text="« Назад", callback_data="start"),
                width=1)
    return builder


def client_show_services_keyboard(client_services_titles, titles_prices):
    """
    Создает клавиатуру с кнопками для выбора услуг.
    :param client_services_titles: Список названий услуг.
    :param titles_prices: Список цен услуг.
    :return: InlineKeyboardBuilder объект с кнопками.
    """
    builder = InlineKeyboardBuilder()
    for i in range(len(client_services_titles)):
        builder.row(
            types.InlineKeyboardButton(text=f"{client_services_titles[i].capitalize()} | {titles_prices[i]}₽",
                                       callback_data=f"client_show_services_{rus_to_eng(client_services_titles[i])}"),
            width=1)
    builder.row(types.InlineKeyboardButton(text="« Назад", callback_data="start"),
                width=1)
    return builder


def client_show_workers_keyboard(workers, title):
    """
    Создает клавиатуру с кнопками для выбора сотрудников, предоставляющих выбранную услугу.
    :param workers: Список сотрудников.
    :param title: Название услуги.
    :return: InlineKeyboardBuilder объект с кнопками.
    """
    builder = InlineKeyboardBuilder()
    for worker in workers:
        builder.row(
            types.InlineKeyboardButton(text=f"{worker['name']} ({worker['rating']}⭐️)",
                                       callback_data=f"client_show_workers_{rus_to_eng(title)}_{worker['id']}"),
            width=1)
    builder.row(types.InlineKeyboardButton(text="« Назад", callback_data=f"client_show_services"),
                width=1)
    return builder


def client_show_worker_keyboard(worker, title):
    """
    Создает клавиатуру для выбранного сотрудника с кнопкой для выбора времени.
    :param worker: Данные сотрудника.
    :param title: Название услуги.
    :return: InlineKeyboardBuilder объект с кнопками.
    """
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Выбрать время",
                                           callback_data=f"client_show_calendar_{worker['id']}_{rus_to_eng(title)}"),
                width=1)
    builder.row(types.InlineKeyboardButton(text="« Назад", callback_data=f"client_show_services_{rus_to_eng(title)}"),
                width=1)
    return builder


def client_show_calendar_dates_keyboard(worker, title, dates):
    """
    Создает клавиатуру с доступными датами для записи.
    :param worker: Данные сотрудника.
    :param title: Название услуги.
    :param dates: Список доступных дат.
    :return: InlineKeyboardBuilder объект с кнопками.
    """
    builder = InlineKeyboardBuilder()
    buttons = []
    k = 0
    for date in dates:
        date_object = datetime.strptime(date, "%Y-%m-%d")
        buttons.append(
            types.InlineKeyboardButton(text=f"{date_object.strftime('%d.%m.%Y')}",
                                       callback_data=f"client_pick_time_{rus_to_eng(title)}_{worker['id']}_{date_object.strftime('%d%m%Y')}"))
    builder.row(*buttons, width=3)
    builder.row(types.InlineKeyboardButton(text='« Назад к "Сотрудникам"',
                                           callback_data=f"client_show_services_{rus_to_eng(title)}"),
                width=1)
    builder.row(types.InlineKeyboardButton(text="« Назад",
                                           callback_data=f"client_show_workers_{rus_to_eng(title)}_{worker['id']}"),
                width=1)
    return builder


def client_show_calendar_times_keyboard(worker, title, date, times):
    """
    Создает клавиатуру с доступным временем для записи.
    :param worker: Данные сотрудника.
    :param title: Название услуги.
    :param date: Дата записи.
    :param times: Список доступного времени.
    :return: InlineKeyboardBuilder объект с кнопками.
    """
    builder = InlineKeyboardBuilder()
    buttons = []
    k = 0
    for time in times:
        time_object = datetime.strptime(time, "%H:%M").time()
        buttons.append(
            types.InlineKeyboardButton(text=f"{time_object.strftime('%H:%M')}",
                                       callback_data=f"client_send_claim_{rus_to_eng(title)}_{worker['id']}_{date}_{time_object.strftime('%H%M')}"))
    builder.row(*buttons, width=3)
    builder.row(types.InlineKeyboardButton(text='« Назад к "Сотрудникам"',
                                           callback_data=f"client_show_services_{rus_to_eng(title)}"),
                width=1)
    builder.row(types.InlineKeyboardButton(text="« Назад",
                                           callback_data=f"client_show_calendar_{worker['id']}_{rus_to_eng(title)}"),
                width=1)
    return builder


def client_send_claim_keyboard(worker, title, date, time_):
    """
    Создает клавиатуру для подтверждения или возврата при отправке заявки.
    :param worker: Данные сотрудника.
    :param title: Название услуги.
    :param date: Дата записи.
    :param time_: Время записи.
    :return: InlineKeyboardBuilder объект с кнопками.
    """
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='Сохранить',
                                           callback_data=f"send_claim_{rus_to_eng(title)}_{worker['id']}_{date}_{time_}"),
                width=1)
    builder.row(types.InlineKeyboardButton(text='« Назад к "Сотрудникам"',
                                           callback_data=f"client_show_services_{rus_to_eng(title)}"),
                width=1)
    builder.row(types.InlineKeyboardButton(text="« Назад",
                                           callback_data=f"client_pick_time_{rus_to_eng(title)}_{worker['id']}_{date}"),
                width=1)
    return builder


def send_claim_keyboard():
    """
    Создает клавиатуру для возврата в главное меню после отправки заявки.
    :return: InlineKeyboardBuilder объект с кнопкой.
    """
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Главное меню »", callback_data=f"start"),
                width=1)
    return builder


def client_show_claims_keyboard(claims):
    """
    Создает клавиатуру для отображения списка заявок пользователя.
    :param claims: Список заявок пользователя.
    :return: InlineKeyboardBuilder объект с кнопками.
    """
    builder = InlineKeyboardBuilder()
    for claim in claims:
        if int(claim[6]) != 2:
            date_object = datetime.strptime(claim[4], "%Y-%m-%d")
            builder.row(
                types.InlineKeyboardButton(text=f"{claim[3].capitalize()} | {date_object.strftime('%d.%m')} {claim[5]}",
                                           callback_data=f"claim_{claim[0]}"),
                width=1)
    builder.row(types.InlineKeyboardButton(text="« Назад", callback_data=f"start"),
                width=1)
    return builder


def claim_keyboard():
    """
    Создает клавиатуру для возврата к списку заявок пользователя.
    :return: InlineKeyboardBuilder объект с кнопкой.
    """
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="« Назад", callback_data=f"client_show_claims"),
                width=1)
    return builder
