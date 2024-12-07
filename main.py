import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import client_handlers_profile, client_handlers_services, client_handlers_claims, client_handlers_admin, master_handlers
from database import db, User, Claim, Admin
from yclients_things import APIClient, DataProcessor


async def on_startup(dp: Dispatcher):
    """
    Инициализация при старте бота.
    Соединение с базой данных и сохранение менеджеров пользователей, заявок и администраторов в диспетчере.
    :param dp: Dispatcher
    :return: None
    """
    await db.connect()
    dp['user_manager'] = User()
    dp['claim_manager'] = Claim()
    dp['admin_manager'] = Admin()
    print('Successful db connect ✅')


async def setup_api(dp: Dispatcher):
    """
    Настройка API YClients.
    Подключение к API YClients, создание дата процессора и сохранение его в диспетчере.
    :param dp: Dispatcher
    :return: None
    """
    api_client = APIClient(
        token="nzdj6eabmyj9kd3mbmjk",
        company_id=1186779,
        form_id=1301768,
        login="hooooogrideeer@gmail.com",
        password="zh33ek"
    )
    data_processor = DataProcessor(api_client.api)
    dp['data_processor'] = data_processor
    print("Successful api connect ✅")


async def main():
    """
    Основная функция запуска бота.
    Запуск бота, создание диспетчера, подключение к базе данных и API
    :return: None
    """
    bot = Bot(token="7349087922:AAF95Y4yHsExdwGzMDQx7GzYOwbEfu27FmI", default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=MemoryStorage())
    await on_startup(dp)
    await setup_api(dp)
    dp.include_routers(client_handlers_profile.router, client_handlers_services.router,
                       client_handlers_claims.router, client_handlers_admin.router, master_handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
