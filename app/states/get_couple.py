from aiogram.dispatcher.filters.state import StatesGroup, State


class GetCouple(StatesGroup):
    GetEvenCouple = State()
    GetOddCouple = State()
    GetNotChangeCouple = State()
