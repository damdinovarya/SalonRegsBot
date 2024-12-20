from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from datetime import datetime
from utils import rus_to_eng


def get_client_tel_keyboard():
    """
    Создает клавиатуру с кнопками для сохранения или редактирования данных пользователя.
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
            state = '🕓'
            if int(claim[6]) == 1:
                state = '✅'
            if int(claim[6]) == 2:
                state = '🤑'
            if int(claim[6]) == 3:
                state = '❌'
            builder.row(
                types.InlineKeyboardButton(text=f"{state} {claim[3].capitalize()} | {date_object.strftime('%d.%m')} {claim[5]}",
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


def await_claim_for_admins(user_id):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Отклонить", callback_data=f"reject_claim_for_admins_{user_id}"),
                width=1)
    builder.row(types.InlineKeyboardButton(text="Принять", callback_data=f"accept_claim_for_admins_{user_id}"),
                width=1)
    return builder


def admin_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Админы", callback_data="admin_show_admins"))
    builder.row(types.InlineKeyboardButton(text="Сотрудники", callback_data="admin_show_workers"))
    builder.row(types.InlineKeyboardButton(text="Заявки", callback_data="admin_show_claims"))
    builder.row(types.InlineKeyboardButton(text="Отправить сообщение", callback_data="admin_send_message"))
    return builder


def admin_show_admins(admins):
    builder = InlineKeyboardBuilder()
    for admin in admins:
        builder.row(types.InlineKeyboardButton(text=f"{' '.join(admin[2].split()[:2])}",
                                               callback_data=f"admin_show_admin_{admin[1]}"))
    builder.row(types.InlineKeyboardButton(text=f"« Назад", callback_data="admin_menu"))
    return builder


def admin_show_admin_():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"« Назад", callback_data="admin_show_admins"))
    return builder


def admin_show_workers(workers):
    builder = InlineKeyboardBuilder()
    for worker in workers:
        builder.row(types.InlineKeyboardButton(text=f"{' '.join(worker['name'].split()[:2])}",
                                               callback_data=f"admin_show_worker_{worker['id']}"))
    builder.row(types.InlineKeyboardButton(text=f"« Назад", callback_data="admin_menu"))
    return builder


def admin_show_worker_(flag, worker_id):
    builder = InlineKeyboardBuilder()
    if flag == 1:
        builder.row(types.InlineKeyboardButton(text=f"Добавить username сотрудника", callback_data=f"admin_add_worker_username_{worker_id}"))
    else:
        builder.row(types.InlineKeyboardButton(text=f"Поменять username сотрудника",
                                               callback_data=f"admin_remove_worker_username_{worker_id}"))
    builder.row(types.InlineKeyboardButton(text=f"« Назад", callback_data="admin_show_workers"))
    return builder


def admin_add_worker_username_(worker_id):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"admin_show_worker_{worker_id}"))
    return builder


def worker_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Новые заказы", callback_data="worker_show_claims_new"))
    builder.row(types.InlineKeyboardButton(text="Выполненные заказы", callback_data="worker_show_completed"))
    builder.row(types.InlineKeyboardButton(text="Отклоненные заказы", callback_data="worker_show_claims_rejected"))
    return builder


def worker_show_claims_new(claims):
    builder = InlineKeyboardBuilder()
    for claim in claims:
        date_object = datetime.strptime(claim[4], "%Y-%m-%d")
        builder.row(
            types.InlineKeyboardButton(text=f"{'🕓' if claim[6] == 0 else '✅'} {claim[3].capitalize()} | {date_object.strftime('%d.%m')} {claim[5]}",
                                       callback_data=f"worker_show_claim_{claim[0]}"),
            width=1)
    builder.row(types.InlineKeyboardButton(text="« Назад", callback_data=f"master_menu"),
                width=1)
    return builder


def worker_show_completed(claims):
    builder = InlineKeyboardBuilder()
    for claim in claims:
        date_object = datetime.strptime(claim[4], "%Y-%m-%d")
        builder.row(
            types.InlineKeyboardButton(text=f"🤑 {claim[3].capitalize()} | {date_object.strftime('%d.%m')} {claim[5]}",
                                       callback_data=f"worker_show_claim_{claim[0]}"),
            width=1)
    builder.row(types.InlineKeyboardButton(text="« Назад", callback_data=f"master_menu"),
                width=1)
    return builder


def worker_show_claims_rejected(claims):
    builder = InlineKeyboardBuilder()
    for claim in claims:
        date_object = datetime.strptime(claim[4], "%Y-%m-%d")
        builder.row(
            types.InlineKeyboardButton(text=f"❌ {claim[3].capitalize()} | {date_object.strftime('%d.%m')} {claim[5]}",
                                       callback_data=f"worker_show_claim_{claim[0]}"),
            width=1)
    builder.row(types.InlineKeyboardButton(text="« Назад", callback_data=f"master_menu"),
                width=1)
    return builder


def worker_show_claim_():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="« Назад", callback_data=f"master_menu"),
                width=1)
    return builder


def send_claim_admin_keyboard(claim_id):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Принять", callback_data=f"admin_answer_claim_{claim_id}_1"),
                width=1)
    builder.row(types.InlineKeyboardButton(text="Отклонить", callback_data=f"admin_answer_claim_{claim_id}_3"),
                width=1)
    return builder
