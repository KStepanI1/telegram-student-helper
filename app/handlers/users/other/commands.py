from aiogram import types
from aiogram.dispatcher.filters import Command

from app.loader import dp
from app.utils.misc import rate_limit


@rate_limit(5, 'commands')
@dp.message_handler(Command("commands"))
async def show_commands(message: types.Message):
    commands_text = [
        "<b>Основные команды</b>:\n",
        "/menu - Меню предметов",
        "/timetable - Показывает расписание",
        "/subscribe - Подписка на уведомления ",
        "/unsubscribe - Отписка от уведомлений",
        "/get_id - Узнать твой user_id",
        "/show_admins - Посмотреть список текущих администраторов",
        "/admin_commands - Команды доступные администраторам"
    ]
    await message.answer("\n".join(commands_text))

