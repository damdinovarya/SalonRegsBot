import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import client_handlers, master_handlers
from database import db
from yclients import APIClient, DataProcessor


async def on_startup():
    await db.connect()
    print('Successful db connect ✅')


async def get_api_data():
    # Создаем экземпляр APIClient для получения данных
    api_client = APIClient(
        token="nzdj6eabmyj9kd3mbmjk",
        company_id=1186779,
        form_id=1301768,
        login="hooooogrideeer@gmail.com",
        password="zh33ek"
    )
    # Получаем данные о сотрудниках и услугах
    staff_data_list, services_data_list = await asyncio.to_thread(api_client.get_data_from_api)

    data_processor = DataProcessor(staff_data_list, services_data_list)

    # Возвращаем обработанные данные для использования в других частях проекта
    return data_processor


async def main():
    await on_startup()
    data_processor = await get_api_data()
    bot = Bot(token="7596895625:AAHBZVnbG2Nee5qxbe5bJ_4-z0luFMCHRZM")
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(client_handlers.router, master_handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
