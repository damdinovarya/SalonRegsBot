import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import client_handlers_profile, client_handlers_services, master_handlers
from database import db
from yclients_things import APIClient, DataProcessor


async def on_startup():
    await db.connect()
    print('Successful db connect ✅')


async def setup_api(dp: Dispatcher):
    """
    Подключение к API YClients и сохранение обработанных данных в диспетчере.
    """
    api_client = APIClient(
        token="nzdj6eabmyj9kd3mbmjk",
        company_id=1186779,
        form_id=1301768,
        login="hooooogrideeer@gmail.com",
        password="zh33ek"
    )
    staff_data_list, services_data_list = await asyncio.to_thread(api_client.get_data_from_api)
    data_processor = DataProcessor(staff_data_list, services_data_list)
    dp['data_processor'] = data_processor
    print("Successful api connect ✅")


async def main():
    await on_startup()
    bot = Bot(token="7349087922:AAF95Y4yHsExdwGzMDQx7GzYOwbEfu27FmI", default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=MemoryStorage())
    await setup_api(dp)
    dp.include_routers(client_handlers_profile.router, client_handlers_services.router, master_handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
