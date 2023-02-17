import asyncio
from datetime import date, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.start import command_start
from keyboarsds.keyboards import get_main_keyboard, get_inline_keyboard, get_inline_keyboard_for_employee
from loader import dp, bot
from states.global_states import Global


from utils.orm_functions import get_all_new_orders, create_employee, upgrate_order_status


@dp.message_handler(lambda message: message.text == 'Хочу выполнить заказ.', state=Global.event)
async def employee_menu(message: types.Message):
    create_employee(message)
    bottoms = ['Показать все открытые заказы.', 'Мои заказы в работе.']
    await message.answer("<b>Меню фрилансера</b>",
                         reply_markup=get_main_keyboard(bottoms))
    await Global.employee_menu.set()

@dp.message_handler(lambda message: message.text == 'Показать все открытые заказы.', state=Global.employee_menu)
async def show_all_orders(message: types.Message, state: FSMContext):
    orders = get_all_new_orders()
    for order in orders:
        await state.update_data(chosen_order=order.id)
        await message.answer(f'<b>Заказчик:</b> {order.user.username}\n'
                             f'<b>ID заказа:</b> {order.id}\n'
                             f'<b>Описание заказа:</b> {order.description_order}\n'
                             f'<b>Дата выполнения заказа:</b> {order.order_date}\n'
                             f'<b>Статус заказа:</b> {order.order_status}\n',
                             reply_markup=get_inline_keyboard_for_employee(order.user.username))
    await Global.show_all_orders.set()

@dp.callback_query_handler(lambda callback_query: callback_query, state=Global.show_all_orders)
async def take_order_to_work(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    print(user_data)
    upgrate_order_status(user_data["chosen_order"], callback)
    await callback.message.delete()
    await callback.answer(text="Заказ взят в работу")
    await state.finish()
