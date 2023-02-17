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


def get_inline_keyboard_for_employee(client):
    сommunication_button = types.InlineKeyboardButton(f'Связаться с заказчиком {client}', url=f't.me/{client}')
    order_button = types.InlineKeyboardButton(text='Принять заказ в работу', callback_data="change_status_order")
    inline_keyboard = types.InlineKeyboardMarkup().add(сommunication_button, order_button)
    return inline_keyboard
