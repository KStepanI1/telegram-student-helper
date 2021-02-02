from aiogram import types
from aiogram.dispatcher.filters import Command

from app.filters.IsAdmin import IsAdminFilter
from app.loader import dp
from app.utils.misc import rate_limit


@rate_limit(5, "admin_commands")
@dp.message_handler(Command("admin_commands"), IsAdminFilter())
async def show_admin_commands(message: types.Message):
    admin_commands_text = [
        "<b>Команды для администратора</b>:\n",
        "/subject - Управление предметами",
        "/event - Управление событиями",
        "/teacher - Управление преподавателями",
        "/timetable_edit - Управление расписанием",
        "/get_admins - Отличается от /show_admins наличием user_name и user_id",
    ]
    await message.answer("\n".join(admin_commands_text))