from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from app.loader import dp
from app.utils.db_api.quick_commands import quick_commands_user as commands
from app.utils.db_api.quick_commands.quick_commands_user import select_user
from app.utils.misc import rate_limit


async def set_user_name(user):
    if user.full_name:
        user_name = user.full_name.split()[0]
    else:
        user_name = user.name
    return user_name


@rate_limit(5, 'start')
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):

    name = message.from_user.full_name
    await commands.add_user(id=message.from_user.id,
                            name=name,
                            subscription=False,
                            admin=False)
    text = [
        f'Приветствую, <b>{name}</b>!',
        f'Можешь написать /help, если впервые 🙈',
        f'Надеюсь тебе понравится то, что я умею /commands',
        f'Удачи!'
    ]
    await message.answer('\n'.join(text))
    await message.answer_sticker(r'CAACAgIAAxkBAAIehGAEMK9g85Zs0HVQHuPbWvr4EqmjAAL3AANWnb0KC3IkHUj0DTAeBA')
