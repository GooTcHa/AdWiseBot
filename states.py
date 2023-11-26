from aiogram.fsm.state import StatesGroup, State


class User(StatesGroup):
    choose_start_action = State()


class Worker(StatesGroup):
    enter_name = State()
    enter_link = State()
    enter_email = State()
    enter_phone = State()
    choose_specialty = State()
    add_new_specialty = State()
    choose_super_power = State()
    choose_duration = State()
    check_cv = State()
    menu = State()
    switch_afk = State()
    look_through_cvs = State()


class Client(StatesGroup):
    menu = State()
    ask_create_project = State()
    ask_delete_project = State()
    enter_title = State()
    choose_spec = State()
    choose_super_power = State()
    enter_descr = State()
    enter_price = State()
    approve_project = State()
    add_new_specialty = State()
    buy_subscription = State()
    choose_project = State()
    choose_specialist = State()
    project_list = State()


class Admin(StatesGroup):
    decline_cv_reason = State()
    decline_project_reason = State()