from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, Bot, types
from yclients_things import DataProcessor
from aiogram.filters import Command
from aiogram.types import Message
from handlers import keyboards
from database import db, User
import datetime
from utils import rus_to_eng, eng_to_rus

router = Router()


class ClientServicesState(StatesGroup):
    user_await = State()


@router.callback_query(F.data == "client_show_services")
async def client_show_services(callback: types.CallbackQuery, state: FSMContext, data_processor: DataProcessor):
    titles = data_processor.get_all_services_titles()
    await callback.message.edit_text(f"Услуги: ", reply_markup=keyboards.client_show_services_keyboard(titles).as_markup())


@router.callback_query(F.data.startswith("client_show_services_"))
async def client_show_services_(callback: types.CallbackQuery, data_processor: DataProcessor):
    title = eng_to_rus(callback.data.split("_")[3])
    await callback.message.edit_text(f"Челики: ",
                                     reply_markup=keyboards.client_show_workers_keyboard(data_processor.get_staff_for_service(title), title).as_markup())


@router.callback_query(F.data.startswith("client_show_workers_"))
async def client_show_workers_(callback: types.CallbackQuery, data_processor: DataProcessor):
    call_data = callback.data.split("_")
    title = eng_to_rus(call_data[3])
    worker = data_processor.get_staff_by_id(int(call_data[4]))
    print(worker)
    await callback.message.edit_media()


@router.message(Command('photo'))
async def send_photo_handler(message: Message):
    # Ссылка на фото
    photo_url = "https://be.cdn.yclients.com/images/no-master-sm.png"

    # Отправляем фото пользователю
    await message.answer_photo(photo=photo_url, caption="Вот ваше фото!")
