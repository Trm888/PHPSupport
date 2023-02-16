from aiogram import types


def get_main_keyboard(buttons: list):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    for button in buttons:
        keyboard.insert(button)
    return keyboard
