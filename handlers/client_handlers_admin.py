from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, types, Bot
from aiogram.filters import Command
from aiogram.types import Message, InputMediaPhoto
from yclients_things import DataProcessor
from handlers import keyboards
from aiogram.types import FSInputFile
from database import Admin, User, Worker
import config
from handlers.keyboards import admin_menu

router = Router()


class ClientAdminState(StatesGroup):
    user_await = State()

    add_worker_username = State()
    update_worker_username = State()


@router.message(Command("admin"))
async def admin(message: Message, user_manager: User, admin_manager: Admin, bot: Bot):
    """
    Панель админа.
    Проверяет наличие админа в базе данных
    запускает регистрацию если его нет
    иначе показывает меню админа.

    :param message:
    :param user_manager:
    :param admin_manager:
    :param bot:
    """
    admin = await admin_manager.get_admin_by_id_telegram(message.chat.id)
    if admin != [] and message.chat.id == admin[1]:
        if admin[2] == 1:
            await message.answer_photo(photo=FSInputFile('handlers/images/admin.jpg'), caption=f"Выберите нужную опцию:",
                                   reply_markup=keyboards.admin_menu().as_markup())
        elif admin[2] == 0:
            await message.answer_photo(photo=FSInputFile('handlers/images/salonregs.jpg'),
                                       caption=f"Ваша заявка на админку на рассмотрении. Ожидайте подтверждения."
                                               f"\n\nНажмите /start для возврата в главное меню.")
        elif admin[2] == 2:
            await message.answer_photo(photo=FSInputFile('handlers/images/salonregs.jpg'),
                                       caption=f"Вы больше не являетесь админом("
                                               f"\n\nНажмите /start для возврата в главное меню.")
        elif admin[2] == 3:
            await message.answer_photo(photo=FSInputFile('handlers/images/salonregs.jpg'),
                                       caption=f"Ваша заявка на админку отклонена("
                                               f"\n\nНажмите /start для возврата в главное меню.")
    else:
        user_data = await user_manager.get_user_by_id_telegram(message.chat.id)
        await admin_manager.create_admin(message.chat.id)
        await bot.send_message(config.ADMIN_ID, f"<b>ЗАЯВКА НА АДМИНКУ</b>"
                                                f"\n\n<b>{user_data[2]}</b>"
                                                f"\n<b>Телефон:</b> {user_data[3]}"
                                                f"\n\nЧтобы принять заявку нажмите на <b>«Принять»</b>",
                               reply_markup=keyboards.await_claim_for_admins(message.chat.id).as_markup())

        await message.answer_photo(photo=FSInputFile('handlers/images/salonregs.jpg'),
                                   caption=f"Ваша заявка на админку на рассмотрении. Ожидайте подтверждения."
                                           f"\n\nНажмите /start для возврата в главное меню.")


@router.callback_query(F.data == "admin_menu")
async def admin_menu(callback: types.CallbackQuery, user_manager: User, admin_manager: Admin):
    """
    Выдает меню админки (Callback).

    :param callback:
    :param user_manager:
    :param admin_manager:
    :return:
    """
    await callback.message.edit_caption(caption=f"Выберите нужную опцию:",
                                      reply_markup=keyboards.admin_menu().as_markup())

@router.callback_query(F.data.startswith("accept_claim_for_admins_"))
async def accept_claim_for_admins_(callback: types.CallbackQuery, user_manager: User, admin_manager: Admin, bot: Bot):
    """
    Одобрение заявки на админку.

    :param callback:
    :param user_manager:
    :param admin_manager:
    :param bot:
    """
    user_id = int(callback.data.split("_")[4])
    user_data = await user_manager.get_user_by_id_telegram(user_id)
    await admin_manager.accept_admin(user_id)
    await callback.message.edit_text(f"<b>ЗАЯВКА НА АДМИНКУ - Одобрена</b>"
                                            f"\n\n<b>{user_data[2]}</b>"
                                            f"\n<b>Телефон:</b> {user_data[3]}"
                                            f"\n\nНажмите /admin чтобы посмотреть меню админа.")

    await bot.send_message(user_id, f"<b>ВАША ЗАЯВКА НА АДМИНКУ ОДОБРЕНА</b>"
                                            f"\nНажмите /admin чтобы посмотреть меню админа")


@router.callback_query(F.data.startswith("reject_claim_for_admins_"))
async def reject_claim_for_admins_(callback: types.CallbackQuery, user_manager: User, admin_manager: Admin):
    """
    Отклонение заявки на админку.

    :param callback:
    :param user_manager:
    :param admin_manager:
    """
    user_id = int(callback.data.split("_")[4])
    user_data = await user_manager.get_user_by_id_telegram(user_id)
    await admin_manager.reject_admin(user_id)
    await callback.message.edit_text(f"<b>ЗАЯВКА НА АДМИНКУ - Отклонена</b>"
                                            f"\n\n<b>{user_data[2]}</b>"
                                            f"\n<b>Телефон:</b> {user_data[3]}"
                                            f"\n\nНажмите /admin чтобы посмотреть меню админа.")


@router.callback_query(F.data == "admin_show_admins")
async def admin_show_admins(callback: types.CallbackQuery, user_manager: User, admin_manager: Admin):
    """
    Выдает админу список всех активных админов.

    :param callback:
    :param user_manager:
    :param admin_manager:
    :return:
    """
    admins_ids = await admin_manager.get_all_admins()
    admins = []
    for admin_id in admins_ids:
        admins.append(await user_manager.get_user_by_id_telegram(admin_id[1]))
    await callback.message.edit_caption(caption=f"Вот список действующих админов:",
                                        reply_markup=keyboards.admin_show_admins(admins).as_markup())


@router.callback_query(F.data.startswith("admin_show_admin_"))
async def admin_show_admin_(callback: types.CallbackQuery, user_manager: User):
    """
    Показывает информацию об выбранном админе.

    :param callback:
    :param user_manager:
    """
    admin_id = int(callback.data.split("_")[3])
    user_data = await user_manager.get_user_by_id_telegram(admin_id)
    await callback.message.edit_caption(caption=f"<b>АДМИН - Статус: активный</b>"
                                            f"\n\n<b>{user_data[2]}</b>"
                                            f"\n<b>Телефон:</b> {user_data[3]}",
                                     reply_markup=keyboards.admin_show_admin_().as_markup())


@router.callback_query(F.data == "admin_show_workers")
async def admin_show_workers(callback: types.CallbackQuery, data_processor: DataProcessor):
    """
    Выдает админу список всех активных сотрудников.

    :param callback:
    :param data_processor:
    :return:
    """
    await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile('handlers/images/admin.jpg'),
                                                            caption=f"Вот список всех действующих сотрудников:"),
                                      reply_markup=keyboards.admin_show_workers(data_processor.get_all_staffs()).as_markup())


@router.callback_query(F.data.startswith("admin_show_worker_"))
async def admin_show_admin_(callback: types.CallbackQuery, worker_manager: Worker,
                            data_processor: DataProcessor, state: FSMContext):
    """
    Показывает информацию об выбранном сотруднике.

    :param callback:
    :param worker_manager:
    :param data_processor:
    :param state:
    """

    worker_id = int(callback.data.split("_")[3])
    worker_database = await worker_manager.get_worker_by_staff_id(int(worker_id))
    flag = 0
    if not worker_database:
        flag = 1
        worker_database = [-1, -1, "Нет в базе данных", worker_id]
    worker = data_processor.get_staff_by_id(int(worker_id))
    await callback.message.edit_media(media=InputMediaPhoto(media=worker['avatar_big'],
                              caption=f"<b>{worker['name']}</b> ({worker['rating']}⭐️)"
                                      f"\n<i>Специализация: {worker['specialization']}</i>"
                                      f"\n\n<pre>{worker['information'].replace('<p>', '').replace('</p>', '')}</pre>"
                                      f"\n\n<b>Telegram ID:</b> {'Не указан' if worker_database[1] == -1 else worker_database[1]}"
                                      f"\n<b>Telegram username:</b> {worker_database[2]}"
                                      f"\n<b>YClients Staff ID:</b> {worker_database[3]}"),
                                      reply_markup=keyboards.admin_show_worker_(flag, worker_id).as_markup())
    await state.clear()


@router.callback_query(F.data.startswith("admin_add_worker_username_"))
async def admin_add_worker_username_(callback: types.CallbackQuery, worker_manager: Worker,
                                     data_processor: DataProcessor, state: FSMContext):
    """
    Включает режим ожидания получения username сотрудника.

    :param callback:
    :param worker_manager:
    :param data_processor:
    :param state:
    """
    worker_id = int(callback.data.split("_")[4])
    await state.set_state(ClientAdminState.add_worker_username)
    await state.update_data(worker_id=worker_id)
    await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile('handlers/images/admin.jpg'),
                                                            caption=f"Отправьте username сотрудника: (Пример: @salon_regs_bot)"),
                                      reply_markup=keyboards.admin_add_worker_username_(worker_id).as_markup())


@router.message(ClientAdminState.add_worker_username)
async def add_worker_username(message: Message, worker_manager: Worker, data_processor: DataProcessor, state: FSMContext):
    """
    Добавляет username выбранному сотруднику.

    :param message:
    :param worker_manager:
    :param data_processor:
    :param state:
    :return:
    """
    username = message.text
    data = await state.get_data()
    worker_id = data['worker_id']
    await worker_manager.create_worker(username, worker_id)
    worker_database = await worker_manager.get_worker_by_staff_id(int(worker_id))
    flag = 0
    if not worker_database:
        flag = 1
        worker_database = [-1, -1, "Нет в базе данных", worker_id]
    worker = data_processor.get_staff_by_id(int(worker_id))
    await message.answer_photo(photo=worker['avatar_big'],
                                 caption=f"<b>{worker['name']}</b> ({worker['rating']}⭐️)"
                                         f"\n<i>Специализация: {worker['specialization']}</i>"
                                         f"\n\n<pre>{worker['information'].replace('<p>', '').replace('</p>', '')}</pre>"
                                         f"\n\n<b>Telegram ID:</b> {'Не указан' if worker_database[1] == -1 else worker_database[1]}"
                                         f"\n<b>Telegram username:</b> {worker_database[2]}"
                                         f"\n<b>YClients Staff ID:</b> {worker_database[3]}",
                                 reply_markup=keyboards.admin_show_worker_(flag, worker_id).as_markup())
    await state.clear()


@router.callback_query(F.data.startswith("admin_remove_worker_username_"))
async def admin_remove_worker_username_(callback: types.CallbackQuery, worker_manager: Worker,
                                     data_processor: DataProcessor, state: FSMContext):
    """
    Включает режим ожидания получения нового username сотрудника.

    :param callback:
    :param worker_manager:
    :param data_processor:
    :param state:
    """
    worker_id = int(callback.data.split("_")[4])
    await state.set_state(ClientAdminState.update_worker_username)
    await state.update_data(worker_id=worker_id)
    await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile('handlers/images/admin.jpg'),
                                                            caption=f"Отправьте новый username сотрудника: (Пример: @salon_regs_bot)"),
                                      reply_markup=keyboards.admin_add_worker_username_(worker_id).as_markup())


@router.message(ClientAdminState.update_worker_username)
async def update_worker_username(message: Message, worker_manager: Worker, data_processor: DataProcessor, state: FSMContext):
    """
    Добавляет новый username выбранному сотруднику.

    :param message:
    :param worker_manager:
    :param data_processor:
    :param state:
    :return:
    """
    username = message.text
    data = await state.get_data()
    worker_id = data['worker_id']
    await worker_manager.update_worker_username(username, worker_id)
    worker_database = await worker_manager.get_worker_by_staff_id(int(worker_id))
    flag = 0
    if not worker_database:
        flag = 1
        worker_database = [-1, -1, "Нет в базе данных", worker_id]
    worker = data_processor.get_staff_by_id(int(worker_id))
    await message.answer_photo(photo=worker['avatar_big'],
                                 caption=f"<b>{worker['name']}</b> ({worker['rating']}⭐️)"
                                         f"\n<i>Специализация: {worker['specialization']}</i>"
                                         f"\n\n<pre>{worker['information'].replace('<p>', '').replace('</p>', '')}</pre>"
                                         f"\n\n<b>Telegram ID:</b> {'Не указан' if worker_database[1] == -1 else worker_database[1]}"
                                         f"\n<b>Telegram username:</b> {worker_database[2]}"
                                         f"\n<b>YClients Staff ID:</b> {worker_database[3]}",
                                 reply_markup=keyboards.admin_show_worker_(flag, worker_id).as_markup())
    await state.clear()