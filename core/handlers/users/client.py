import asyncio
from datetime import date, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.start import command_start
from keyboarsds.keyboards import get_main_keyboard
from loader import dp, bot
from states.global_states import Global

import os
import django

from utils.orm_functions import get_client_order

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()

from phpsupport.models import User, Order


@dp.message_handler(lambda message: message.text == 'Хочу разместить заказ.', state=Global.event)
async def client_menu(message: types.Message):
    bottoms = ['Cоздать заказ.', 'Мои заказы.']
    await message.answer("<b>Меню клиента</b>",
                         reply_markup=get_main_keyboard(bottoms))
    await Global.client_menu.set()


@dp.message_handler(lambda message: message.text == 'Cоздать заказ.', state=Global.client_menu)
async def client_menu(message: types.Message):
    await message.answer(
        'Описание заказа:',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await Global.description_order.set()


@dp.message_handler(lambda message: message.text.count(' ') < 3,
                    state=Global.description_order)
async def get_valid_name(message: types.Message):
    await message.reply(
        'Опешите свой заказ подробнее')


@dp.message_handler(state=Global.description_order)
async def order_date(message: types.Message, state: FSMContext):
    await state.update_data(description_order=message.text)
    await state.update_data(username=message.from_user.username)
    date_list = []
    for i in range(10):
        date_list.append(str(date.today() + timedelta(days=i)))
    print(date_list)
    await message.answer(
        'К какой дате нужно закончить заказ:',
        reply_markup=get_main_keyboard(date_list)
    )
    await Global.order_date.set()


@dp.message_handler(state=Global.order_date)
async def order_finish(message: types.Message, state: FSMContext):
    await state.update_data(order_date=message.text)
    user_data = await state.get_data()
    await message.answer(
        '<b>Ваш заказ создан и отправлен в работу.</b>')
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'<b>Пользователь: {user_data["username"]}\n'
                                f'Описание заказа: {user_data["description_order"]}\n'
                                f'Дата окончания заказа: {user_data["order_date"]}</b>')

    get_client_order(message, user_data["description_order"], user_data["order_date"])
    await state.finish()
    await asyncio.sleep(3)
    await command_start(message)


@dp.message_handler(lambda message: message.text == 'Мои заказы.', state=Global.client_menu)
async def client_menu(message: types.Message):
    await message.answer(
        '<b>Здесь будет функция получения заказов размещенные клиентому.</b>')
    # получить заказы пользователя
    pass