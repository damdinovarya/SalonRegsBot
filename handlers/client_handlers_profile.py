from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, InputMediaPhoto
from handlers import keyboards
from aiogram.types import FSInputFile
from database import User

router = Router()


class ClientProfileState(StatesGroup):
    """
    Состояния пользователя для регистрации.
    """
    user_await = State()

    get_client_name = State()
    get_client_tel = State()

    edit_client_name = State()
    edit_client_tel = State()


@router.message(Command("start"))
async def start(message: Message, state: FSMContext, user_manager: User):
    """
    Начало
    Проверяет наличие пользователя в базе данных
    запускает регистрацию если его нет
    иначе показывает меню.

    :param message:
    :param state:
    :param user_manager:
    """
    users = await user_manager.get_users()
    users_ids = [i[1] for i in users]
    if message.chat.id in users_ids:
        await message.answer_photo(photo=FSInputFile('handlers/images/menu.jpg'), caption=f"Выберите нужную опцию:",
                                   reply_markup=keyboards.client_menu_keyboard().as_markup())
    else:
        await message.answer_photo(photo=FSInputFile('handlers/images/salonregs.jpg'),
                                   caption=f"Привет! Я бот для регистрации в салон красоты. Отправь мне свое ФИО:")
        await state.set_state(ClientProfileState.get_client_name)


@router.callback_query(F.data == "start")
async def start_callback(callback: types.CallbackQuery, state: FSMContext, user_manager: User):
    """
    callback в меню
    Проверяет наличие пользователя в базе данных
    запускает регистрацию если его нет
    иначе показывает меню.

    :param callback:
    :param state:
    :param user_manager:
    """
    users = await user_manager.get_users()
    users_ids = [i[1] for i in users]
    if callback.message.chat.id in users_ids:
        await callback.message.edit_media(
            media=InputMediaPhoto(media=FSInputFile('handlers/images/menu.jpg'), caption=f"Выберите нужную опцию:"),
            reply_markup=keyboards.client_menu_keyboard().as_markup())
    else:
        await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile('handlers/images/salonregs.jpg'),
                                                                caption=f"Привет! Я бот для регистраций в салон красоты. Отправь мне свое ФИО:"))
        await state.set_state(ClientProfileState.get_client_name)


# REGISTRATION
@router.message(ClientProfileState.get_client_name)
async def get_client_name(message: Message, state: FSMContext):
    """
    Обрабатывает ввод ФИО пользователя.
    Переходит к запросу номера телефона или повторно запрашивает корректное ФИО.

    :param message:
    :param state:
    """
    client_name = message.text
    if len(client_name.split()) >= 2:
        await state.update_data(client_name=client_name)
        await message.answer(f"Приятно познакомиться, {client_name}!\n\n"
                             f"Напишите ваш номер телефона:")
        await state.set_state(ClientProfileState.get_client_tel)
    else:
        await message.answer(
            f"К сожалению, этих данных недостаточно( "
            f"Проверьте наличие фамилии или имени и отправьте мне ФИО повторно:")
        await state.set_state(ClientProfileState.get_client_name)


@router.message(ClientProfileState.get_client_tel)
async def get_client_tel(message: Message, state: FSMContext):
    """
    Обрабатывает ввод номера телефона пользователя.
    Завершение регистрации или повторное редактирование профиля.

    :param message:
    :param state:
    """
    client_tel = message.text
    await state.update_data(client_tel=client_tel)
    await state.set_state(ClientProfileState.user_await)
    user_data = await state.get_data()
    await message.answer_photo(photo=FSInputFile('handlers/images/salonregs.jpg'),
                               caption=f"<b>ВАШИ ДАННЫЕ</b>"
                                       f"\n\n<b>Имя:</b> {user_data['client_name']}"
                                       f"\n<b>Телефон:</b> {user_data['client_tel']}"
                                       f"\n\n<i>Выберите следующий шаг:</i>",
                               reply_markup=keyboards.get_client_tel_keyboard().as_markup())


@router.message(F.data == "user_await")
async def user_await_state(message: Message, state: FSMContext):
    """
    Режим ожидания пользователя.

    :param message:
    :param state:
    :return:
    """
    user_data = await state.get_data()
    await message.answer_photo(photo=FSInputFile('handlers/images/salonregs.jpg'),
                               caption=f"<b>ВАШИ ДАННЫЕ</b>"
                                       f"\n\n<b>Имя:</b> {user_data['client_name']}"
                                       f"\n<b>Телефон:</b> {user_data['client_tel']}"
                                       f"\n\n<i>Выберите следующий шаг:</i>",
                               reply_markup=keyboards.get_client_tel_keyboard().as_markup())
    await state.set_state(ClientProfileState.user_await)


# EDIT USER
@router.callback_query(F.data == "client_data_edit")
async def client_data_edit_callback(callback: types.CallbackQuery, state: FSMContext, user_manager: User):
    """
    Переход к редактированию профиля пользователя.

    :param callback:
    :param state:
    :param user_manager:
    """
    users = await user_manager.get_users()
    users_ids = [i[1] for i in users]
    user_data = await state.get_data()
    if callback.message.chat.id in users_ids and 'client_name' not in user_data:
        user_db_data = await user_manager.get_user_by_id_telegram(callback.message.chat.id)
        await state.update_data(client_name=user_db_data[2])
        await state.update_data(client_tel=user_db_data[3])
        user_data = await state.get_data()
        await callback.message.edit_caption(caption=f"Выберите, что изменить.",
                                            reply_markup=keyboards.client_data_edit_keyboard(user_data["client_name"],
                                                                                             user_data[
                                                                                                 "client_tel"]).as_markup())
    elif callback.message.chat.id not in users_ids and 'client_name' not in user_data:
        await callback.message.edit_caption(caption=f"К сожалению мы не смогли сохранить твои прошлые данные, "
                                                    f"давай знакомиться сначала! Напиши мне свое ФИО:")
        await state.set_state(ClientProfileState.get_client_name)
    else:
        await callback.message.edit_caption(caption=f"Выберите, что изменить.",
                                            reply_markup=keyboards.client_data_edit_keyboard(user_data["client_name"],
                                                                                             user_data[
                                                                                                 "client_tel"]).as_markup())


@router.callback_query(F.data == "client_data_edit_name")
async def client_data_edit_name_callback(callback: types.CallbackQuery, state: FSMContext):
    """
    Редактирование имени пользователя.
    Ставит статус ожидания ввода нового ФИО пользователя.

    :param callback:
    :param state:
    :return:
    """
    await callback.message.edit_caption(caption=f"Отправь мне заново свое ФИО:")
    await state.set_state(ClientProfileState.edit_client_name)


@router.callback_query(F.data == "client_data_edit_tel")
async def client_data_edit_tel_callback(callback: types.CallbackQuery, state: FSMContext):
    """
    Редактирование номера телефона пользователя.
    Ставит статус ожидания ввода нового номера телефона пользователя.

    :param callback:
    :param state:
    :return:
    """
    await callback.message.edit_caption(caption=f"Отправь мне заново свой номер телефона:")
    await state.set_state(ClientProfileState.edit_client_tel)


@router.message(ClientProfileState.edit_client_name)
async def edit_client_name_state(message: Message, state: FSMContext):
    """
    Обрабатывает ввод нового имени пользователя.

    :param message:
    :param state:
    :return:
    """
    client_name = message.text
    if len(client_name.split()) >= 2:
        await state.update_data(client_name=client_name)
        await state.set_state(ClientProfileState.user_await)
        user_data = await state.get_data()
        await message.answer_photo(photo=FSInputFile('handlers/images/salonregs.jpg'),
                                   caption=f"<b>ВАШИ ДАННЫЕ</b>"
                                           f"\n\n<b>Имя:</b> {user_data['client_name']}"
                                           f"\n<b>Телефон:</b> {user_data['client_tel']}"
                                           f"\n\n<i>Выберите следующий шаг:</i>",
                                   reply_markup=keyboards.get_client_tel_keyboard().as_markup())
    else:
        await message.answer(f"К сожалению, этих данных недостаточно( "
                             f"Проверьте наличие фамилии или имени и отправьте мне ФИО повторно:")
        await state.set_state(ClientProfileState.edit_client_name)


@router.message(ClientProfileState.edit_client_tel)
async def edit_client_tel_state(message: Message, state: FSMContext):
    """
    Обрабатывает ввод нового телефона пользователя.

    :param message:
    :param state:
    :return:
    """
    client_tel = message.text
    await state.update_data(client_tel=client_tel)
    await state.set_state(ClientProfileState.user_await)
    user_data = await state.get_data()
    await message.answer_photo(photo=FSInputFile('handlers/images/salonregs.jpg'),
                               caption=f"<b>ВАШИ ДАННЫЕ</b>"
                                       f"\n\n<b>Имя:</b> {user_data['client_name']}"
                                       f"\n<b>Телефон:</b> {user_data['client_tel']}"
                                       f"\n\n<i>Выберите следующий шаг:</i>",
                               reply_markup=keyboards.get_client_tel_keyboard().as_markup())
    await state.set_state(ClientProfileState.user_await)


# SAVE USER
@router.callback_query(F.data == "client_data_save")
async def client_data_save_callback(callback: types.CallbackQuery, state: FSMContext, user_manager: User):
    """
    Сохраняет данные профиля пользователя в базу данных.
    Обновляет существующий профиль или создает новый.

    :param callback:
    :param state:
    :param user_manager:
    """
    user_data = await state.get_data()
    users = await user_manager.get_users()
    users_ids = [i[1] for i in users]
    if callback.message.chat.id not in users_ids:
        await user_manager.create_user(callback.message.chat.id, user_data["client_name"], user_data["client_tel"])
    else:
        await user_manager.update_user(callback.message.chat.id, user_data["client_name"], user_data["client_tel"])
    await callback.message.edit_media(
        media=InputMediaPhoto(media=FSInputFile('handlers/images/menu.jpg'), caption=f"Данные сохранены. Меню: "),
        reply_markup=keyboards.client_menu_keyboard().as_markup())
    await state.clear()


# SHOW USER PROFILE
@router.callback_query(F.data == "client_show_profile")
async def client_show_profile_callback(callback: types.CallbackQuery, user_manager: User):
    """
    Показывает профиль пользователя из базы данных.

    :param callback:
    :param user_manager:
    """
    user_data = await user_manager.get_user_by_id_telegram(callback.message.chat.id)
    await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile('handlers/images/profile.jpg'),
                                                            caption=f"<b>{user_data[2]}</b>"
                                                                    f"\n<b>Телефон:</b> {user_data[3]}\n"
                                                                    f"\n\n<i>Если хотите изменить данные, нажмите на кнопку «Редактировать»</i>"),
                                      reply_markup=keyboards.client_show_profile_keyboard().as_markup())
