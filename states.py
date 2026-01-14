# states.py
from aiogram.fsm.state import StatesGroup, State

class ConvertStates(StatesGroup):
    waiting_for_amount = State()
    waiting_for_from_currency = State()
    waiting_for_to_currency = State()

class FavoriteStates(StatesGroup):
    waiting_for_from = State()
    waiting_for_to = State()

class CommissionStates(StatesGroup):
    waiting_for_amount = State()
    waiting_for_rate = State()
    waiting_for_commission = State()

class TipsStates(StatesGroup):
    waiting_for_bill = State()
    waiting_for_people = State()
    waiting_for_tip = State()