from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F, types, Bot
from yclients_things import DataProcessor
from aiogram.types import FSInputFile, InputMediaPhoto
from handlers import keyboards
from database import User, Claim, Worker
from datetime import datetime
from utils import eng_to_rus

router = Router()


class ClientServicesState(StatesGroup):
    """
    Состояния пользователя для выбора и оформления услуг.
    """
    user_await = State()


@router.callback_query(F.data == "client_show_services")
async def client_show_services(callback: types.CallbackQuery, data_processor: DataProcessor):
    """
    Показывает список доступных услуг.

    :param callback:
    :param data_processor: Объект для обработки данных из YClients API.
    """
    titles, titles_prices = data_processor.get_all_services_titles()
    await callback.message.edit_media(
        media=InputMediaPhoto(media=FSInputFile('handlers/images/services.jpg'), caption="Вот наши услуги:"),
        reply_markup=keyboards.client_show_services_keyboard(titles, titles_prices).as_markup())


@router.callback_query(F.data.startswith("client_show_services_"))
async def client_show_services_(callback: types.CallbackQuery, data_processor: DataProcessor):
    """
    Показывает список сотрудников, оказывающие выбранную услугу.

    :param callback:
    :param data_processor: Объект для работы с данными из YClients API.
    """
    title = eng_to_rus(callback.data.split("_")[3])
    await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile('handlers/images/workers.jpg'),
                                                            caption=f"Выбранная услуга: {title.capitalize()}"
                                                                    f"\n\nВыберите сотрудника:"),
                                      reply_markup=keyboards.client_show_workers_keyboard(
                                          data_processor.get_staff_for_service(title), title).as_markup())


@router.callback_query(F.data.startswith("client_show_workers_"))
async def client_show_workers_(callback: types.CallbackQuery, data_processor: DataProcessor):
    """
    Показывает информацию о сотруднике и его специализации.

    :param callback:
    :param data_processor: Объект для работы с данными из YClients API.
    """
    call_data = callback.data.split("_")
    title = eng_to_rus(call_data[3])
    price = data_processor.get_service_price_by_name(title)
    worker = data_processor.get_staff_by_id(int(call_data[4]))
    await callback.message.edit_media(media=InputMediaPhoto(media=worker['avatar_big'],
                                                            caption=f"<b>{worker['name']}</b> ({worker['rating']}⭐️)"
                                                                    f"\n<i>Специализация: {worker['specialization']}</i>"
                                                                    f"\n\n<pre>{worker['information'].replace('<p>', '').replace('</p>', '')}</pre>"
                                                                    f"\n\n<b>Выбранная услуга:</b> {title.capitalize()}"
                                                                    f"\n<b>Стоимость услуги:</b> {price}₽"),
                                      reply_markup=keyboards.client_show_worker_keyboard(worker, title).as_markup())


@router.callback_query(F.data.startswith("client_show_calendar_"))
async def client_show_calendar_(callback: types.CallbackQuery, data_processor: DataProcessor):
    """
    Показывает календарь с доступными датами для записи к сотруднику.

    :param callback:
    :param data_processor: Объект для работы с данными из YClients API.
    """
    call_data = callback.data.split("_")
    title = eng_to_rus(call_data[4])
    price = data_processor.get_service_price_by_name(title)
    worker = data_processor.get_staff_by_id(int(call_data[3]))
    dates = data_processor.get_staff_dates(worker['id'])
    await callback.message.edit_caption(caption=f"<b>{worker['name']}</b> ({worker['rating']}⭐️)"
                                                f"\n<i>Специализация: {worker['specialization']}</i>"
                                                f"\n\n<pre>{worker['information'].replace('<p>', '').replace('</p>', '')}</pre>"
                                                f"\n\n<b>Выбранная услуга:</b> {title.capitalize()}"
                                                f"\n<b>Стоимость услуги:</b> {price}₽"
                                                f"\n\nВыберите свободную дату:",
                                        reply_markup=keyboards.client_show_calendar_dates_keyboard(worker, title,
                                                                                                   dates).as_markup())


@router.callback_query(F.data.startswith("client_pick_time_"))
async def client_pick_time_(callback: types.CallbackQuery, data_processor: DataProcessor):
    """
    Показывает доступное время для выбранной даты и сотрудника.

    :param callback:
    :param data_processor: Объект для работы с данными из YClients API.
    """
    call_data = callback.data.split("_")
    title = eng_to_rus(call_data[3])
    price = data_processor.get_service_price_by_name(title)
    worker = data_processor.get_staff_by_id(int(call_data[4]))
    date_object = datetime.strptime(call_data[5], "%d%m%Y")
    times = data_processor.get_staff_dates_times(worker['id'], title, date_object.strftime('%Y-%m-%d'))
    await callback.message.edit_caption(caption=f"<b>{worker['name']}</b> ({worker['rating']}⭐️)"
                                                f"\n<i>Специализация: {worker['specialization']}</i>"
                                                f"\n\n<pre>{worker['information'].replace('<p>', '').replace('</p>', '')}</pre>"
                                                f"\n\n<b>Выбранная услуга:</b> {title.capitalize()}"
                                                f"\n<b>Стоимость услуги:</b> {price}₽"
                                                f"\n<b>Дата:</b> {date_object.strftime('%d.%m.%Y')}"
                                                f"\n\nВыберите время:",
                                        reply_markup=keyboards.client_show_calendar_times_keyboard(worker, title,
                                                                                                   call_data[5],
                                                                                                   times).as_markup())


@router.callback_query(F.data.startswith("client_send_claim_"))
async def client_send_claim_(callback: types.CallbackQuery, data_processor: DataProcessor):
    """
    Показывает предварительную заявку пользователя.

    :param callback:
    :param data_processor: Объект для обработки данных из YClients API.
    """
    call_data = callback.data.split("_")
    title = eng_to_rus(call_data[3])
    price = data_processor.get_service_price_by_name(title)
    worker = data_processor.get_staff_by_id(int(call_data[4]))
    date_object = datetime.strptime(call_data[5], "%d%m%Y")
    time_object = datetime.strptime(call_data[6], "%H%M").time()
    await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile('handlers/images/claim.jpg'),
                                                            caption=f"<b>ВАША ЗАЯВКА:</b>"
                                                                    f"\n\n<b>Сотрудник:</b> {worker['name']} ({worker['rating']}⭐️)"
                                                                    f"\n<b>Выбранная услуга:</b> {title.capitalize()}"
                                                                    f"\n<b>Стоимость услуги:</b> {price}₽"
                                                                    f"\n<b>Дата:</b> {date_object.strftime('%d.%m.%Y')}"
                                                                    f"\n<b>Время:</b> {time_object.strftime('%H:%M')}"
                                                                    f"\n\n<i>Внимательно проверьте данные, если нужно что-то изменить нажмите на кнопку «Назад»</i>"),
                                      reply_markup=keyboards.client_send_claim_keyboard(worker, title, call_data[5],
                                                                                        call_data[6]).as_markup())


@router.callback_query(F.data.startswith("send_claim_"))
async def send_claim_(callback: types.CallbackQuery, data_processor: DataProcessor, user_manager: User,
                      claim_manager: Claim, worker_manager: Worker, bot: Bot):
    """
    Сохраняет заявку в базу данных и уведомляет пользователя о её отправке.

    :param callback:
    :param data_processor: Объект для обработки данных из YClients API.
    :param user_manager: Менеджер для работы с базой данных клиентов.
    :param claim_manager: Менеджер для работы с базой данных заявок.
    :param worker_manager: Менеджер для работы с базой данных сотрудника.
    :param bot:
    """
    call_data = callback.data.split("_")
    title = eng_to_rus(call_data[2])
    price = data_processor.get_service_price_by_name(title)
    worker = data_processor.get_staff_by_id(int(call_data[3]))
    date_object = datetime.strptime(call_data[4], "%d%m%Y")
    time_object = datetime.strptime(call_data[5], "%H%M").time()
    user = await user_manager.get_user_by_id_telegram(callback.message.chat.id)
    await claim_manager.create_claim(user[1], worker['id'], title, date_object.strftime('%Y-%m-%d'),
                                     time_object.strftime('%H:%M'))
    worker_all_data = await worker_manager.get_worker_by_staff_id(worker['id'])
    claim = await claim_manager.get_claim_by_all_param(user[1], worker['id'], title, date_object.strftime('%Y-%m-%d'),
                                     time_object.strftime('%H:%M'))
    print(claim)
    if worker_all_data and worker_all_data[1] != -1:
        await bot.send_message(worker_all_data[1], f"<b>НОВАЯ ЗАЯВКА</b>"
                                                    f"\n\nЗаказчик: {user[2]}"
                                                    f"\nTelegram: @{callback.from_user.username}"
                                                    f"\n\n<b>Выбранная услуга:</b> {title.capitalize()}"
                                                    f"\n<b>Стоимость услуги:</b> {price}₽"
                                                    f"\n<b>Дата:</b> {date_object.strftime('%d.%m.%Y')}"
                                                    f"\n<b>Время:</b> {time_object.strftime('%H:%M')}",
                               reply_markup=keyboards.send_claim_admin_keyboard(claim[0]).as_markup())

    await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile('handlers/images/sended.jpg'),
                                                            caption=f"<b>ВАША ЗАЯВКА ОТПРАВЛЕНА</b> | <i>Статус:</i> на рассмотрении 🕓"
                                                                    f"\n\n<b>Сотрудник:</b> {worker['name']} ({worker['rating']}⭐️)"
                                                                    f"\n<b>Выбранная услуга:</b> {title.capitalize()}"
                                                                    f"\n<b>Стоимость услуги:</b> {price}₽"
                                                                    f"\n<b>Дата:</b> {date_object.strftime('%d.%m.%Y')}"
                                                                    f"\n<b>Время:</b> {time_object.strftime('%H:%M')}"
                                                                    f"\n\n<i>Ожидайте подтверждение заявки, ответ придет в ближайшее время</i>"),
                                      reply_markup=keyboards.send_claim_keyboard().as_markup())
