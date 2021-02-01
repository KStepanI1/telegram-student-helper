from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("menu", "Меню предметов"),
        types.BotCommand("timetable", "Посмотреть расписание"),
        types.BotCommand("commands", "Посмотреть список команд"),
        types.BotCommand("subscribe", "Подписаться на уведомления"),
        types.BotCommand("unsubscribe", "Отписаться от уведомлений"),
        types.BotCommand("/get_id - Узнать твой user_id"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("/show_admins - Посмотреть список текущих администраторов"),
        types.BotCommand("admin_commands", "Команды доступные админам"),
    ])
