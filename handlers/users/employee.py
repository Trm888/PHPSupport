import asyncio

from aiogram import types
from keyboarsds.keyboards import get_main_keyboard, get_inline_keyboard_for_employee, \
    get_inline_keyboard_next_two_orders, get_inline_keyboard_for_employee_with_my_orders
from loader import dp, bot, STRITE_TOKEN
from states.global_states import Global
from utils.orm_functions import get_all_new_orders, create_employee, upgrate_order_status, get_employee_orders, \
    upgrate_order_status_complete, get_employee_done_orders, get_employee

orders = get_all_new_orders()
current_item = 0
PRICE = types.LabeledPrice(label='Подписка на 1 месяц', amount=50000)


@dp.message_handler(lambda message: message.text == 'Хочу выполнить заказ.', state=Global.event)
async def employee_menu(message: types.Message):
    create_employee(message)
    employee = get_employee(message)
    if not employee.subscription:
        await message.answer("<b>Прежде чем продожить, нужно оплатить подписку.</b>")
        await bot.send_invoice(message.chat.id,
                               title='Подписка на бота',
                               provider_token=STRITE_TOKEN,
                               currency='rub',
                               description='Подписка на бота',
                               is_flexible=False,
                               prices=[PRICE],
                               start_parameter='one_month_subscription',
                               payload='test_invoice_payload')
        await Global.buy_subscription_employee.set()
    else:
        bottoms = ['Показать все открытые заказы.', 'Мои заказы в работе.', 'Архив заказов.']
        await message.answer("<b>Меню фрилансера:</b>",
                             reply_markup=get_main_keyboard(bottoms))
        await Global.employee_menu.set()


@dp.pre_checkout_query_handler(lambda query: query.invoice_payload == 'test_invoice_payload',
                               state=Global.buy_subscription_employee)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    await Global.employee_subscription_buy.set()


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT, state=Global.employee_subscription_buy)
async def successful_payment(message: types.Message):
    employee = get_employee(message)
    employee.subscription = True
    employee.save()
    bottoms = ['Показать все открытые заказы.', 'Мои заказы в работе.', 'Архив заказов.']
    await message.answer("<b>Меню фрилансера:</b>",
                         reply_markup=get_main_keyboard(bottoms))
    await Global.employee_menu.set()


@dp.message_handler(lambda message: message.text == 'Мои заказы в работе.', state=Global.employee_menu)
async def show_my_orders(message: types.Message):
    orders = get_employee_orders(message)
    if orders:
        for order in orders:
            await message.answer(f'<b>Заказчик:</b> {order.user.username}\n'
                                 f'<b>ID заказа:</b> {order.id}\n'
                                 f'<b>Описание заказа:</b> {order.description_order}\n'
                                 f'<b>Дата выполнения заказа:</b> {order.order_date}\n'
                                 f'<b>Статус заказа:</b> {order.order_status}\n',
                                 reply_markup=get_inline_keyboard_for_employee_with_my_orders(order.user.username,
                                                                                              order.id))

        await asyncio.sleep(1)
        await employee_menu(message)
    else:
        await message.answer('У вас нет заказов в работе.')
        await asyncio.sleep(1)
        await employee_menu(message)


@dp.message_handler(lambda message: message.text == 'Архив заказов.', state=Global.employee_menu)
async def show_my_orders(message: types.Message):
    orders = get_employee_done_orders(message)
    if orders:
        for order in orders:
            await message.answer(f'<b>Заказчик:</b> {order.user.username}\n'
                                 f'<b>ID заказа:</b> {order.id}\n'
                                 f'<b>Описание заказа:</b> {order.description_order}\n'
                                 f'<b>Дата выполнения заказа:</b> {order.order_date}\n'
                                 f'<b>Статус заказа:</b> {order.order_status}\n')

        await asyncio.sleep(1)
        await employee_menu(message)
    else:
        await message.answer('У вас нет выполненных заказов.')
        await asyncio.sleep(1)
        await employee_menu(message)


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'next_two_order',
                           state=Global.employee_menu)
async def show_next_orders(callback: types.CallbackQuery):
    global current_item
    order1 = orders[current_item]
    order2 = orders[(current_item + 1) % len(orders)]
    current_item = (current_item + 2) % len(orders)
    await callback.message.answer(f'<b>Заказчик:</b> {order1.user.username}\n'
                                  f'<b>ID заказа:</b> {order1.id}\n'
                                  f'<b>Описание заказа:</b> {order1.description_order}\n'
                                  f'<b>Дата выполнения заказа:</b> {order1.order_date}\n'
                                  f'<b>Статус заказа:</b> {order1.order_status}\n',
                                  reply_markup=get_inline_keyboard_for_employee(order1.user.username, order1.id))
    await callback.message.answer(f'<b>Заказчик:</b> {order2.user.username}\n'
                                  f'<b>ID заказа:</b> {order2.id}\n'
                                  f'<b>Описание заказа:</b> {order2.description_order}\n'
                                  f'<b>Дата выполнения заказа:</b> {order2.order_date}\n'
                                  f'<b>Статус заказа:</b> {order2.order_status}\n',
                                  reply_markup=get_inline_keyboard_next_two_orders(order2.user.username, order2.id))
    await Global.employee_menu.set()


@dp.message_handler(lambda message: message.text == 'Показать все открытые заказы.', state=Global.employee_menu)
async def show_open_orders(message: types.Message):
    global current_item
    current_item = 0
    if len(orders) > 2:
        order1 = orders[current_item]
        order2 = orders[(current_item + 1) % len(orders)]
        current_item = (current_item + 2) % len(orders)
        await message.reply(f'<b>Заказчик:</b> {order1.user.username}\n'
                            f'<b>ID заказа:</b> {order1.id}\n'
                            f'<b>Описание заказа:</b> {order1.description_order}\n'
                            f'<b>Дата выполнения заказа:</b> {order1.order_date}\n'
                            f'<b>Статус заказа:</b> {order1.order_status}\n',
                            reply_markup=get_inline_keyboard_for_employee(order1.user.username, order1.id))
        await message.reply(f'<b>Заказчик:</b> {order2.user.username}\n'
                            f'<b>ID заказа:</b> {order2.id}\n'
                            f'<b>Описание заказа:</b> {order2.description_order}\n'
                            f'<b>Дата выполнения заказа:</b> {order2.order_date}\n'
                            f'<b>Статус заказа:</b> {order2.order_status}\n',
                            reply_markup=get_inline_keyboard_next_two_orders(order2.user.username, order2.id))
        await Global.employee_menu.set()
        await asyncio.sleep(1)
        await employee_menu(message)
    elif len(orders) == 2:
        order1 = orders[current_item]
        order2 = orders[(current_item + 1) % len(orders)]
        await message.reply(f'<b>Заказчик:</b> {order1.user.username}\n'
                            f'<b>ID заказа:</b> {order1.id}\n'
                            f'<b>Описание заказа:</b> {order1.description_order}\n'
                            f'<b>Дата выполнения заказа:</b> {order1.order_date}\n'
                            f'<b>Статус заказа:</b> {order1.order_status}\n',
                            reply_markup=get_inline_keyboard_for_employee(order1.user.username, order1.id))
        await message.reply(f'<b>Заказчик:</b> {order2.user.username}\n'
                            f'<b>ID заказа:</b> {order2.id}\n'
                            f'<b>Описание заказа:</b> {order2.description_order}\n'
                            f'<b>Дата выполнения заказа:</b> {order2.order_date}\n'
                            f'<b>Статус заказа:</b> {order2.order_status}\n',
                            reply_markup=get_inline_keyboard_for_employee(order2.user.username, order2.id))
        await Global.employee_menu.set()
        await asyncio.sleep(1)
        await employee_menu(message)
    elif len(orders) == 1:
        await message.reply(f'<b>Заказчик:</b> {orders[0].user.username}\n'
                            f'<b>ID заказа:</b> {orders[0].id}\n'
                            f'<b>Описание заказа:</b> {orders[0].description_order}\n'
                            f'<b>Дата выполнения заказа:</b> {orders[0].order_date}\n'
                            f'<b>Статус заказа:</b> {orders[0].order_status}\n',
                            reply_markup=get_inline_keyboard_for_employee(orders[0].user.username, orders[0].id))
        await Global.employee_menu.set()
        await asyncio.sleep(1)
        await employee_menu(message)
    else:
        await message.reply('Нет открытых заказов')
        await asyncio.sleep(1)
        await employee_menu(message)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('call:'),
                           state=Global.employee_menu)
async def take_order_to_work(callback: types.CallbackQuery):
    global orders
    print(callback.data[5:])
    order_id = int(callback.data[5:])
    upgrate_order_status(order_id, callback)
    await callback.message.delete()
    await callback.answer(text="Заказ взят в работу")
    orders = get_all_new_orders()


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('change_status:'),
                           state=Global.employee_menu)
async def take_order_to_work(callback: types.CallbackQuery):
    print(callback.data[14:])
    order_id = int(callback.data[14:])
    upgrate_order_status_complete(order_id)
    await callback.message.delete()
    await callback.answer(text="Заказ выполнен и отправлен в архив")
