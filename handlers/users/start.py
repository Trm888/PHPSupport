from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboarsds.keyboards import get_main_keyboard
from loader import dp
from states.global_states import Global


# from transitions.transitions import *
# from utils.get_nearest_salon import *
# from utils.orm_functions import *


@dp.message_handler(commands="start", state="*")
async def command_start(message: types.Message):
    # user, created_user = User.objects.get_or_create(chat_id=message.chat.id)
    # print(user, created_user)
    bottoms = ['Хочу выполнить заказ.', 'Хочу оформить заказ.']
    await message.reply("<b>Добро пожаловать! Вас приветствует бот который связывает клиентов и фрилансеров</b>",
                        reply_markup=get_main_keyboard(bottoms))
    await Global.event.set()
