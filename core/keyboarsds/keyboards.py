from aiogram import types


def get_main_keyboard(buttons: list):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    for button in buttons:
        keyboard.insert(button)
    return keyboard


def get_inline_keyboard(employee):
    order_button = types.InlineKeyboardButton(f'Связаться с исполнителем {employee}', url=f't.me/{employee}')
    inline_keyboard = types.InlineKeyboardMarkup().add(order_button)
    return inline_keyboard


def get_inline_keyboard_for_employee_with_my_orders(client, order_id):
    сommunication_button = types.InlineKeyboardButton(f'Связаться с заказчиком {client}', url=f't.me/{client}')
    order_button = types.InlineKeyboardButton(text='Изменить статус заказа', callback_data=f"change_status:{order_id}")
    inline_keyboard = types.InlineKeyboardMarkup().add(сommunication_button, order_button)
    return inline_keyboard


def get_inline_keyboard_for_employee(client, order_id):
    сommunication_button = types.InlineKeyboardButton(f'Связаться с заказчиком {client}', url=f't.me/{client}')
    order_button = types.InlineKeyboardButton(text='Принять заказ в работу', callback_data=f"call:{order_id}")
    inline_keyboard = types.InlineKeyboardMarkup().add(сommunication_button, order_button)
    return inline_keyboard


def get_inline_keyboard_next_two_orders(client, order_id):
    сommunication_button = types.InlineKeyboardButton(f'Связаться с заказчиком {client}', url=f't.me/{client}')
    order_button = types.InlineKeyboardButton(text='Принять заказ в работу', callback_data=f"call:{order_id}")
    next_order_button = types.InlineKeyboardButton(text='Показать 2 следующих заказа', callback_data="next_two_order")
    inline_keyboard = types.InlineKeyboardMarkup(row_width=2).add(сommunication_button, order_button, next_order_button)
    return inline_keyboard
