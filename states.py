from aiogram.fsm.state import StatesGroup, State

class Registration(StatesGroup):
    waiting_for_contact = State()
    waiting_for_name = State()
    waiting_for_profession = State()
    waiting_for_payment = State()
