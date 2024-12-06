from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, Bot, types
from yclients_things import DataProcessor
from aiogram.filters import Command
from aiogram.types import Message
from handlers import keyboards
from database import db, User
import datetime

router = Router()

class ClientServicesState(StatesGroup):
    user_await = State()

@router.callback_query(F.data == "client_show_services")
async def client_show_services(callback: types.CallbackQuery, state: FSMContext, data_processor: DataProcessor):
    print(data_processor)
    await callback.message.answer(f"Меню: ", reply_markup=keyboards.client_menu_keyboard().as_markup())
