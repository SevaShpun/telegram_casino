import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor
from config import BOT_TOKEN

loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage, loop=loop)


async def anti_flood(*args, **kwargs):
    m = args[0]
    await m.answer("Не флуди...")


if __name__ == "__main__":
    from handlers import dp, sand_to_admin
    executor.start_polling(dp, on_startup=sand_to_admin)
