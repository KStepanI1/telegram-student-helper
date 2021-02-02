from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from app.loader import dp
from app.utils.db_api.quick_commands import quick_commands_user as commands
from app.utils.db_api.quick_commands.quick_commands_user import select_user
from app.utils.misc import rate_limit


@rate_limit(5, 'start')
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = await select_user(message.from_user.id)
    name = message.from_user.full_name
    if not user:
        await commands.add_user(id=message.from_user.id,
                                name=name,
                                subscription=False,
                                admin=False)
    else:
        user_subscription = user.subscription
        user_admin_status = user.admin
        if not user_subscription:
            user_subscription = False
        if not user_admin_status:
            user_admin_status = False
        await commands.update_user(id=message.from_user.id,
                                   name=name,
                                   subscription=user_subscription,
                                   admin=user_admin_status)
    text = [
        f'Приветствую, <b>{name}</b>!',
        f'Можешь написать /help, если впервые 🙈',
        f'Надеюсь тебе понравится то, что я умею: /commands'
    ]
    await message.answer('\n'.join(text))
    await message.answer_sticker(r'CAACAgIAAxkBAAIehGAEMK9g85Zs0HVQHuPbWvr4EqmjAAL3AANWnb0KC3IkHUj0DTAeBA')
