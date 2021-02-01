from aiogram import types
from aiogram.dispatcher.filters import CommandHelp

from app.loader import dp
from app.utils.misc import rate_limit


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp())
async def show_help(message: types.Message):
    await message.answer("Я не знаю что сюда писать, тут и так все понятно\n"
                         "/commands - команда которая тебе поможет")
    await message.answer_sticker("CAACAgEAAxkBAAIexWAEQne8DPUzSJcFUD04nTb5tNR-AAJ5DwACmX-IAuGMHI9M_qbfHgQ")

