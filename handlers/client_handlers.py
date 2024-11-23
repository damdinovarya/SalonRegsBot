from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, Bot, types
from aiogram.filters import Command
from aiogram.types import Message
from handlers import keyboards
from database import db, User
import datetime

router = Router()


class client_state(StatesGroup):
    get_client_name = State()
    get_client_tel = State()

    edit_client_name = State()
    edit_client_tel = State()


@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    user_manager = User()
    users = await user_manager.get_users()
    users_ids = [i[1] for i in users]
    if message.chat.id in users_ids:
        await message.answer(f"Меню")
    else:
        await message.answer(f"Привет! Я бот для регистраций на мероприятия DC. Отправь мне свое ФИО:")
        await state.set_state(client_state.get_client_name)


@router.message(client_state.get_client_name)
async def get_client_name(message: Message, state: FSMContext):
    client_name = message.text
    if len(client_name.split()) >= 2:
        await state.update_data(client_name=client_name)
        await message.answer(f"Приятно познакомиться, {client_name}!\n\n"
                             f"Напишите ваш номер телефона:")
        await state.set_state(client_state.get_client_tel)
    else:
        await message.answer(
            f"К сожалению, этих данных недостаточно( Проверьте наличие фамилии или имени и отправьте мне ФИО повторно:")
        await state.set_state(client_state.get_client_name)


@router.message(client_state.get_client_tel)
async def get_client_tel(message: Message, state: FSMContext):
    client_tel = message.text
    await state.update_data(client_tel=client_tel)
    user_data = await state.get_data()
    await message.answer(f"Ваши данные: \n "
                         f"Имя: {user_data['client_name']}\n "
                         f"Телефон: {user_data['client_tel']}",
                         reply_markup=keyboards.get_client_tel_keyboard().as_markup())
    await state.set_state(client_state.get_client_tel)


@router.callback_query(F.data == "client_data_save")
async def client_data_save_callback(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_manager = User()
    await user_manager.create_user(callback.message.chat.id, user_data["client_name"], user_data["client_tel"])
    await callback.message.edit_text(f"Данные сохранены. Меню ")
    await state.clear()


@router.callback_query(F.data == "client_data_edit")
async def client_data_edit_callback(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await callback.message.edit_text(f"Выберите, что изменить.",
                                     reply_markup=keyboards.client_data_edit_keyboard(user_data["client_name"],
                                                                                      user_data["client_tel"]).as_markup())

#
# @router.callback_query(F.data == "client_data_edit_name")
# async def client_data_edit_name_callback(callback: types.CallbackQuery, state: FSMContext):
#
