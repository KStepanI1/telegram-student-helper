from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from app.keyboards.inline.timetable_keyboards.timetable_keyboard import timetable_cd, set_days_keyboard, \
    set_timetable_for_day_keyboard
from app.loader import dp, bot
from app.utils.db_api.quick_commands.quick_commands_timetable import select_all_couples_for_day
from app.utils.misc import rate_limit
from app.utils.misc.texts.timetable import days, couple_text
from app.utils.misc.timetable.parser_status_of_the_week import StatusOfTheWeek


async def update_date():
    global date
    date = await StatusOfTheWeek().parse()


async def set_text_for_timetable(day_of_week, status_of_the_week):
    couples = await select_all_couples_for_day(day_of_week)
    check_couples = False
    couple_number = 1
    text_for_timetable = [f"Расписание на день недели <b>{days[day_of_week]}</b>"]
    for couple in couples:
        if status_of_the_week == "1":
            name_couple = couple.name_couple_odd
        else:
            name_couple = couple.name_couple_even
        if name_couple:
            check_couples = True
            text_for_timetable.append(couple_text.format(
                couple_number=couple_number,
                time_start=couple.time_start,
                name_couple=name_couple,
                time_end=couple.time_end,
                time_break=couple.time_break
            ))
        couple_number += 1
    if not check_couples:
        text_for_timetable.append(f"\nЗанятий на день недели <b>{days[day_of_week]}</b> не было добавлено")
    return text_for_timetable


@rate_limit(5, 'timetable')
@dp.message_handler(Command("timetable"))
async def show_timetable_menu(message: types.Message):
    status_of_the_week = date.split()[1]
    await show_list_days(message, status_of_the_week)


async def show_list_days(message: Union[types.Message, types.CallbackQuery], status_of_the_week, **kwargs):
    markup = await set_days_keyboard(status_of_the_week)
    status_text = {"1": "нечетную", "2": "четную"}
    if isinstance(message, types.Message):
        await message.answer(
            f"Расписание на <b>{status_text[status_of_the_week]}</b> неделю\n<b>Сегодня</b>: {date}",
            reply_markup=markup
        )

    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.answer()
        await call.message.edit_text(
            f"Расписание на <b>{status_text[status_of_the_week]}</b> неделю\n<b>Сегодня</b>: {date}",
            reply_markup=markup
        )


async def show_timetable(call: CallbackQuery, day_of_the_week, status_of_the_week, **kwargs):
    markup = await set_timetable_for_day_keyboard(status_of_the_week)
    await call.answer()
    text_for_timetable = await set_text_for_timetable(day_of_the_week, status_of_the_week)
    await call.message.edit_text(text="\n".join(text_for_timetable), reply_markup=markup)


async def finish_timetable(call: CallbackQuery, **kwargs):
    await bot.delete_message(call.message.chat.id, call.message.message_id)


@dp.callback_query_handler(timetable_cd.filter())
async def timetable_navigation(call: types.CallbackQuery, callback_data: dict):
    current_level = callback_data.get("level")
    day_of_the_week = callback_data.get("day_of_the_week")
    status_of_the_week = callback_data.get("status_of_the_week")

    levels = {
        "-1": finish_timetable,
        "0": show_list_days,
        "1": show_timetable,
    }
    current_level_function = levels[current_level]

    await current_level_function(
        call,
        level=current_level,
        day_of_the_week=day_of_the_week,
        status_of_the_week=status_of_the_week
    )
