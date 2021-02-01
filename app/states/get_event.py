from aiogram.dispatcher.filters.state import StatesGroup, State


class GetEvent(StatesGroup):
    GetName = State()
    GetDate = State()
    GetTime = State()
    WaitPress = State()

