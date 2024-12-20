from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, types, Bot
from aiogram.filters import Command
from aiogram.types import Message, InputMediaPhoto
from yclients_things import DataProcessor
from handlers import keyboards
from aiogram.types import FSInputFile
from database import Admin, User, Worker, Claim
from datetime import datetime
import config
from handlers.keyboards import admin_menu

router = Router()


class MasterState(StatesGroup):
    user_await = State()

@router.message(Command("master"))
async def master(message: Message, worker_manager: Worker):
    """
    Панель сотрудника.
    Проверяет наличие сотрудника в базе данных
    регистрирует если его нет
    иначе показывает меню сотрудника.

    :param message:
    :param worker_manager:
    """
    username = "@" + str(message.from_user.username)
    worker = await worker_manager.get_worker_by_username(username)
    if username not in worker:
        await message.answer_photo(photo=FSInputFile('handlers/images/admin.jpg'),
                                   caption=f"К сожалению вас нет в нашей базе данных(( "
                                           f"Напишите вашему администратору, чтобы добавил ваш username в базу."
                                           f"\n\nНажмите /start чтобы вернуться в главное меню.")
    else:
        if message.chat.id not in worker:
            await worker_manager.update_worker(message.chat.id, username)
        await message.answer_photo(photo=FSInputFile('handlers/images/master.jpg'),
                                   caption=f"Вот меню сотрудника:", reply_markup=keyboards.worker_menu().as_markup())


@router.callback_query(F.data == "master_menu")
async def master_menu(callback: types.CallbackQuery, worker_manager: Worker):
    """
    Выдает сотруднику список всех новых невыполненных заказов.

    :param callback:
    :param worker_manager:
    :return:
    """
    await callback.message.edit_caption(caption=f"Вот меню сотрудника:",
                                        reply_markup=keyboards.worker_menu().as_markup())



@router.callback_query(F.data == "worker_show_claims_new")
async def worker_show_claims_new(callback: types.CallbackQuery, worker_manager: Worker, claim_manager: Claim):
    """
    Выдает сотруднику список всех новых невыполненных заказов.

    :param callback:
    :param worker_manager:
    :param claim_manager:
    :return:
    """
    worker = await worker_manager.get_worker_by_user_id(callback.message.chat.id)
    all_claims = await claim_manager.get_claim_by_master(worker[3])
    claims = [claim for claim in all_claims if claim[6] in [0, 1]]
    await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile('handlers/images/admin.jpg'),
                                                            caption=f"Вот список всех невыполненных заказов:"),
                                      reply_markup=keyboards.worker_show_claims_new(claims).as_markup())


@router.callback_query(F.data == "worker_show_completed")
async def worker_show_completed(callback: types.CallbackQuery, worker_manager: Worker, claim_manager: Claim):
    """
    Выдает сотруднику список всех новых невыполненных заказов.

    :param callback:
    :param worker_manager:
    :param claim_manager:
    :return:
    """
    worker = await worker_manager.get_worker_by_user_id(callback.message.chat.id)
    all_claims = await claim_manager.get_claim_by_master(worker[3])
    claims = [claim for claim in all_claims if claim[6] in [2]]
    await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile('handlers/images/admin.jpg'),
                                                            caption=f"Вот список всех выполненных заказов:"),
                                      reply_markup=keyboards.worker_show_completed(claims).as_markup())


@router.callback_query(F.data == "worker_show_claims_rejected")
async def worker_show_claims_rejected(callback: types.CallbackQuery, worker_manager: Worker, claim_manager: Claim):
    """
    Выдает сотруднику список всех новых невыполненных заказов.

    :param callback:
    :param worker_manager:
    :param claim_manager:
    :return:
    """
    worker = await worker_manager.get_worker_by_user_id(callback.message.chat.id)
    all_claims = await claim_manager.get_claim_by_master(worker[3])
    claims = [claim for claim in all_claims if claim[6] in [3]]
    await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile('handlers/images/admin.jpg'),
                                                            caption=f"Вот список всех отмененных заказов:"),
                                      reply_markup=keyboards.worker_show_claims_rejected(claims).as_markup())


@router.callback_query(F.data.startswith("worker_show_claim_"))
async def claim_(callback: types.CallbackQuery, user_manager: User,
                 data_processor: DataProcessor, claim_manager: Claim, bot: Bot):
    """
    Показывает информацию о конкретной заявке.

    :param callback:
    :param user_manager:
    :param data_processor: Объект для обработки данных из YClients API.
    :param claim_manager: Менеджер для работы с базой данных заявок.
    :param bot:
    """
    claim_id = int(callback.data.split("_")[3])
    claim = await claim_manager.get_claim_by_id(claim_id)
    worker = data_processor.get_staff_by_id(int(claim[2]))
    price = data_processor.get_service_price_by_name(claim[3])
    date_object = datetime.strptime(claim[4], "%Y-%m-%d")
    time_object = datetime.strptime(claim[5], "%H:%M").time()
    state = 'на рассмотрении 🕓'
    if int(claim[6]) == 1:
        state = 'одобрена ✅'
    if int(claim[6]) == 2:
        state = 'исполнена 🤑'
    if int(claim[6]) == 3:
        state = 'отклонена ❌'
    user = await user_manager.get_user_by_id_telegram(claim[1])
    user_username = await bot.get_chat(claim[1])
    await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile('handlers/images/claim.jpg'),
                                                            caption=f"<b>ЗАЯВКА</b> | <i>Статус:</i> {state}"
                                                                    f"\n\nЗаказчик: {user[2]}"
                                                                    f"\nTelegram: @{user_username.username}"
                                                                    f"\n\n<b>Сотрудник:</b> {worker['name']} ({worker['rating']}⭐️)"
                                                                    f"\n<b>Выбранная услуга:</b> {claim[3].capitalize()}"
                                                                    f"\n<b>Стоимость услуги:</b> {price}₽"
                                                                    f"\n<b>Дата:</b> {date_object.strftime('%d.%m.%Y')}"
                                                                    f"\n<b>Время:</b> {time_object.strftime('%H:%M')}"),
                                      reply_markup=keyboards.worker_show_claim_().as_markup())


@router.callback_query(F.data.startswith("admin_answer_claim_"))
async def admin_answer_claim_(callback: types.CallbackQuery, user_manager: User,
                 data_processor: DataProcessor, claim_manager: Claim, bot: Bot):
    """
    Показывает информацию о конкретной заявке.

    :param callback:
    :param user_manager:
    :param data_processor: Объект для обработки данных из YClients API.
    :param claim_manager: Менеджер для работы с базой данных заявок.
    :param bot:
    """
    claim_id = int(callback.data.split("_")[3])
    state_n = int(callback.data.split("_")[4])
    await claim_manager.update_claim_state(claim_id, state_n)
    claim = await claim_manager.get_claim_by_id(claim_id)
    state = 'на рассмотрении 🕓'
    if int(claim[6]) == 1:
        state = 'одобрена ✅'
    if int(claim[6]) == 2:
        state = 'исполнена 🤑'
    if int(claim[6]) == 3:
        state = 'отклонена ❌'
    worker = data_processor.get_staff_by_id(int(claim[2]))
    price = data_processor.get_service_price_by_name(claim[3])
    date_object = datetime.strptime(claim[4], "%Y-%m-%d")
    time_object = datetime.strptime(claim[5], "%H:%M").time()
    user = await user_manager.get_user_by_id_telegram(claim[1])
    user_username = await bot.get_chat(user[1])
    await callback.message.edit_text(f"<b>ЗАЯВКА</b> | <i>Статус:</i> {state}"
                                    f"\n\nЗаказчик: {user[2]}"
                                    f"\nTelegram: @{user_username.username}"
                                    f"\n\n<b>Сотрудник:</b> {worker['name']} ({worker['rating']}⭐️)"
                                    f"\n<b>Выбранная услуга:</b> {claim[3].capitalize()}"
                                    f"\n<b>Стоимость услуги:</b> {price}₽"
                                    f"\n<b>Дата:</b> {date_object.strftime('%d.%m.%Y')}"
                                    f"\n<b>Время:</b> {time_object.strftime('%H:%M')}"
                                    f"\n\nНажмите /master чтобы посмотреть меню сотрудника.")

    await bot.send_message(user[1], f"<b>ОТКЛИК ПО ЗАЯВКЕ</b> | <i>Статус:</i> {state}"
                                                    f"\n\n<b>Сотрудник:</b> {worker['name']} ({worker['rating']}⭐️)"
                                                    f"\n<b>Выбранная услуга:</b> {claim[3].capitalize()}"
                                                    f"\n<b>Стоимость услуги:</b> {price}₽"
                                                    f"\n<b>Дата:</b> {date_object.strftime('%d.%m.%Y')}"
                                                    f"\n<b>Время:</b> {time_object.strftime('%H:%M')}"
                                                    f"\n\nНажмите на /start чтобы попасть в главное меню.")