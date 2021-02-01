from aiogram.dispatcher.filters.state import StatesGroup, State


class GetAdmin(StatesGroup):
    GetId = State()
    GetFullname = State()


class DeleteAdmin(StatesGroup):
    GetId = State()