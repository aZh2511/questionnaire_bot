from aiogram import executor
import asyncio
from config import admin_id
from loader import bot


async def on_shutdown(dp):
    await bot.close()


async def on_startup(dp):
    await asyncio.sleep(2)
    await bot.send_message(admin_id, "Я запущен!")


if __name__ == '__main__':
    from user import dp
    from admin import dp

    executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup)
