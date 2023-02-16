import os
import django


from aiogram import types

from keyboarsds.keyboards import get_main_keyboard
from loader import dp
from states.global_states import Global

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
#
django.setup()
#
#
from phpsupport.models import User




@dp.message_handler(commands="start", state="*")
async def command_start(message: types.Message):
    user, created_user = User.objects.get_or_create(chat_id=message.chat.id, username=message.chat.username)
    print(user, created_user)
    print(message.chat.username)
    bottoms = ['Хочу выполнить заказ.', 'Хочу разместить заказ.']
    await message.answer("<b>Добро пожаловать! Вас приветствует бот который связывает клиентов и фрилансеров</b>",
                         reply_markup=get_main_keyboard(bottoms))
    await Global.event.set()
