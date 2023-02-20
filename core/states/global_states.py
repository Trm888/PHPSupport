from aiogram.dispatcher.filters.state import State, StatesGroup


class Global(StatesGroup):
    buy_subscription_client = State()
    buy_subscription_employee = State()
    start = State()
    client_subscription_buy = State()
    employee_subscription_buy = State()
    event = State()
    client_menu = State()
    description_order = State()
    order_date = State()
    employee_menu = State()
