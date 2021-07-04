from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.models.user import select_user, add_user, update_user


async def user_start(message: Message):
    user = await select_user(message.from_user.id)
    full_name = message.from_user.full_name
    username = message.from_user.username if message.from_user.username else "absent"
    if not user:
        await add_user(user_id=message.from_user.id,
                       full_name=full_name,
                       username=username)
    else:
        await update_user(user_id=message.from_user.id,
                          full_name=full_name,
                          username=username)
    text = [
        f'Приветствую, <b>{full_name}</b>!',
        f'Вот мои команды /commands'
    ]
    await message.answer('\n'.join(text))
    await message.answer_sticker(r'CAACAgIAAxkBAAIBMWAZKvfwXxv-KezlYGjUV6Kx2OwKAAIMBwACRvusBPm-gzuXezySHgQ')


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
