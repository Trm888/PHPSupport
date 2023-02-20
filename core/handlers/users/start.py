from aiogram import types

from keyboarsds.keyboards import get_main_keyboard
from loader import dp
from states.global_states import Global


@dp.message_handler(commands="start", state="*")
async def command_start(message: types.Message):
    bottoms = ['Хочу выполнить заказ.', 'Хочу разместить заказ.']
    await message.answer("<b>Добро пожаловать! Вас приветствует бот который связывает клиентов и фрилансеров."
                         "Что желаете?</b>",
                         reply_markup=get_main_keyboard(bottoms)
                         )
    await Global.event.set()
