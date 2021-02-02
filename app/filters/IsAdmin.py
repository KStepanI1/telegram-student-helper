import random

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from app.utils.db_api.quick_commands.quick_commands_user import select_user


class IsAdminFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        user = await select_user(message.from_user.id)
        if not user.admin:
            await message.answer("Этой командой может воспользоваться только администратор")
            await message.answer_sticker("CAACAgIAAxkBAAIBK2AZKqnaH6WRTOsHBEqHajWsOJCMAAISBwACRvusBF4h-F2mRHaRHgQ")
        return user.admin
