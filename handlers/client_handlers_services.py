from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, Bot, types
from yclients_things import DataProcessor
from aiogram.types import FSInputFile, InputMediaPhoto
from aiogram.filters import Command
from aiogram.types import Message
from handlers import keyboards
from database import db, User
import datetime
from utils import rus_to_eng, eng_to_rus
import time

router = Router()


class ClientServicesState(StatesGroup):
    user_await = State()


@router.callback_query(F.data == "client_show_services")
async def client_show_services(callback: types.CallbackQuery, state: FSMContext, data_processor: DataProcessor):
    titles = data_processor.get_all_services_titles()
    await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile('handlers/images/services.jpg'), caption="Услуги:"), reply_markup=keyboards.client_show_services_keyboard(titles).as_markup())


@router.callback_query(F.data.startswith("client_show_services_"))
async def client_show_services_(callback: types.CallbackQuery, data_processor: DataProcessor):
    title = eng_to_rus(callback.data.split("_")[3])
    await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile('handlers/images/workers.jpg'), caption=f"Челики:"),
                                     reply_markup=keyboards.client_show_workers_keyboard(data_processor.get_staff_for_service(title), title).as_markup())


@router.callback_query(F.data.startswith("client_show_workers_"))
async def client_show_workers_(callback: types.CallbackQuery, data_processor: DataProcessor):
    call_data = callback.data.split("_")
    title = eng_to_rus(call_data[3])
    worker = data_processor.get_staff_by_id(int(call_data[4]))
    await callback.message.edit_media(media=InputMediaPhoto(media=worker['avatar_big'],
                                      caption=f"<b>{worker['name']}</b> ({worker['rating']}⭐️)"
                                              f"\n<i>Специализация: {worker['specialization']}</i>"
                                              f"\n\n<pre>{worker['information'].replace('<p>', '').replace('</p>', '')}</pre>"),
                                      reply_markup=keyboards.client_show_worker_keyboard(worker, title).as_markup())
