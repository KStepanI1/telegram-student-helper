from aiogram import types
from aiogram.dispatcher.filters import Command

from app.loader import dp
from app.utils.db_api.quick_commands.quick_commands_user import update_subscribe_status, select_user
from app.utils.misc import rate_limit


@rate_limit(5, 'subscribe')
@dp.message_handler(Command('subscribe'))
async def add_user_to_subscribers(message: types.Message):
    user = await select_user(message.from_user.id)
    if user:
        if not user.subscription:
            await update_subscribe_status(message.from_user.id, subscribe_status=True)
            await message.answer("Вы подписались на уведомление!")
        else:
            await message.answer("Вы уже подписаны")
    else:
        await message.answer("Пропишите /start и повторите попытку")


@rate_limit(5, 'unsubscribe')
@dp.message_handler(Command("unsubscribe"))
async def remove_user_from_subscribers(message: types.Message):
    user = await select_user(message.from_user.id)
    if user:
        if user.subscription:
            await update_subscribe_status(message.from_user.id, subscribe_status=False)
            await message.answer("Вы отписались от уведомлений!")
    else:
        await message.answer("Вы и так не подписаны")
