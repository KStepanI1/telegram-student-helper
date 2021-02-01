from aiogram.dispatcher.filters.state import StatesGroup, State


class GetTeacher(StatesGroup):
    GetName = State()
    GetKind = State()
    GetMail = State()


class EditTeacher(StatesGroup):
    EditName = State()
    EditMail = State()
