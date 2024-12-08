from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F, types
from yclients_things import DataProcessor
from aiogram.types import FSInputFile, InputMediaPhoto
from handlers import keyboards
from database import User, Claim
from datetime import datetime

router = Router()


class ClientClaimsState(StatesGroup):
    user_await = State()


@router.callback_query(F.data == "client_show_claims")
async def client_show_claims(callback: types.CallbackQuery, user_manager: User, claim_manager: Claim):
    """
    Показывает список заявок пользователя.

    :param callback:
    :param user_manager: Менеджер для работы с базой данных клиентов.
    :param claim_manager: Менеджер для работы с базой данных заявок.
    """
    user = await user_manager.get_user_by_id_telegram(callback.message.chat.id)
    claims = await claim_manager.get_claim_by_user_id(user[0])
    await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile('handlers/images/claims.jpg'),
                                                            caption="Вот ваши заявки"),
                                      reply_markup=keyboards.client_show_claims_keyboard(claims).as_markup())


@router.callback_query(F.data.startswith("claim_"))
async def claim_(callback: types.CallbackQuery, data_processor: DataProcessor, user_manager: User,
                 claim_manager: Claim):
    """
    Показывает информацию о конкретной заявке.

    :param callback:
    :param data_processor: Объект для обработки данных из YClients API.
    :param user_manager: Менеджер для работы с базой данных клиентов.
    :param claim_manager: Менеджер для работы с базой данных заявок.
    """
    claim_id = int(callback.data.split("_")[1])
    claim = await claim_manager.get_claim_by_id(claim_id)
    worker = data_processor.get_staff_by_id(int(claim[2]))
    price = data_processor.get_service_price_by_name(claim[3])
    date_object = datetime.strptime(claim[4], "%Y-%m-%d")
    time_object = datetime.strptime(claim[5], "%H:%M").time()
    state = 'на рассмотрении'
    if int(claim[6]) == 1:
        state = 'одобрена'
    if int(claim[6]) == 2:
        state = 'исполнена'
    await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile('handlers/images/claim.jpg'),
                                                            caption=f"<b>ВАША ЗАЯВКА ОТПРАВЛЕНА</b> | <i>Статус:</i> <pre>{state}</pre>"
                                                                    f"\n\n<b>Сотрудник:</b> {worker['name']} ({worker['rating']}⭐️)"
                                                                    f"\n<b>Выбранная услуга:</b> {claim[3].capitalize()}"
                                                                    f"\n<b>Стоимость услуги:</b> {price}₽"
                                                                    f"\n<b>Дата:</b> {date_object.strftime('%d.%m.%Y')}"
                                                                    f"\n<b>Время:</b> {time_object.strftime('%H:%M')}"),
                                      reply_markup=keyboards.claim_keyboard().as_markup())
