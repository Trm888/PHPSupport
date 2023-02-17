from aiogram.dispatcher.filters.state import State, StatesGroup


class Global(StatesGroup):
    event = State()
    client_menu = State()
    description_order = State()
    order_date = State()
    employee_menu = State()
    show_all_orders = State()
    # bouquet = State()
    # person_data = State()
    # registration_name = State()
    # registration_phonenumber = State()
    # cancel = State()
    # address_street = State()
    # address_number_house = State()
    # address_number_flat = State()
    # address_number_driveway = State()
    pass