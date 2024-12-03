import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import client_handlers, master_handlers
from database import db


async def on_startup():
    await db.connect()
    print('Successful db connect ✅')


async def main():
    await on_startup()
    bot = Bot(token="7596895625:AAHBZVnbG2Nee5qxbe5bJ_4-z0luFMCHRZM")
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(client_handlers.router, master_handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
