from aiogram import executor

from handlers import dp
from utils.set_bot_commands import set_default_commands


async def on_startup(dp):
    await set_default_commands(dp)
    print("Бот запущен!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
