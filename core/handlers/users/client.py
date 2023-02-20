import asyncio
from datetime import date, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboarsds.keyboards import get_main_keyboard, get_inline_keyboard
from loader import dp, bot, STRITE_TOKEN
from states.global_states import Global
from utils.orm_functions import get_client_orders, create_client_order, create_user, get_client_done_orders, get_user

PRICE = types.LabeledPrice(label='Подписка на 1 месяц', amount=50000)


@dp.message_handler(lambda message: message.text == 'Хочу разместить заказ.', state=Global.event)
async def client_menu(message: types.Message):
    create_user(message)
    user = get_user(message)
    if not user.subscription:
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
        await Global.buy_subscription_client.set()
    else:
        bottoms = ['Cоздать заказ.', 'Мои заказы в работе.', 'Архив заказов.']
        await message.answer("<b>Меню клиента:</b>",
                             reply_markup=get_main_keyboard(bottoms))
        await Global.client_menu.set()


@dp.pre_checkout_query_handler(lambda query: query.invoice_payload == 'test_invoice_payload',
                               state=Global.buy_subscription_client)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    await Global.client_subscription_buy.set()


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT, state=Global.client_subscription_buy)
async def successful_payment(message: types.Message):
    user = get_user(message)
    user.subscription = True
    user.save()
    bottoms = ['Cоздать заказ.', 'Мои заказы в работе.', 'Архив заказов.']
    await message.answer("<b>Меню клиента:</b>",
                         reply_markup=get_main_keyboard(bottoms))
    await Global.client_menu.set()


@dp.message_handler(lambda message: message.text == 'Cоздать заказ.', state=Global.client_menu)
async def description_order(message: types.Message):
    await message.answer(
        'Описание заказа:',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await Global.description_order.set()


@dp.message_handler(lambda message: message.text.count(' ') < 3,
                    state=Global.description_order)
async def valid_name(message: types.Message):
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

    create_client_order(message, user_data["description_order"], user_data["order_date"])
    await state.finish()
    await asyncio.sleep(1)
    await client_menu(message)


@dp.message_handler(lambda message: message.text == 'Мои заказы в работе.', state=Global.client_menu)
async def client_orders(message: types.Message):
    orders = get_client_orders(message)
    if orders:
        for order in orders:
            if order.employee:
                await bot.send_message(chat_id=message.from_user.id,
                                       text=f'<b>Пользователь: {order.user.username}\n'
                                            f'Описание заказа: {order.description_order}\n'
                                            f'Дата окончания заказа: {order.order_date}\n'
                                            f'Статус заказа: {order.order_status}\n'
                                            f'Исполнитель: {order.employee}</b>',
                                       reply_markup=get_inline_keyboard(order.employee))
            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text=f'<b>Пользователь: {order.user.username}\n'
                                            f'Описание заказа: {order.description_order}\n'
                                            f'Дата окончания заказа: {order.order_date}\n'
                                            f'Статус заказа: {order.order_status}</b>')

        await asyncio.sleep(3)
        await client_menu(message)
    else:
        await message.answer(
            '<b>У вас нет заказов.</b>')
        await asyncio.sleep(3)
        await client_menu(message)


@dp.message_handler(lambda message: message.text == 'Архив заказов.', state=Global.client_menu)
async def show_my_orders(message: types.Message):
    orders = get_client_done_orders(message)
    if orders:
        for order in orders:
            await message.answer(f'<b>Заказчик: {order.user.username}\n'
                                 f'ID заказа: {order.id}\n'
                                 f'Описание заказа: {order.description_order}\n'
                                 f'Дата выполнения заказа: {order.order_date}\n'
                                 f'Статус заказа: {order.order_status}\n'
                                 f'Исполнитель: {order.employee}</b>')

        await asyncio.sleep(1)
        await client_menu(message)
    else:
        await message.answer('У вас нет выполненных заказов.')
        await asyncio.sleep(1)
        await client_menu(message)
