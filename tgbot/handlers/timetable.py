import logging
from datetime import datetime, timedelta
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery
from asgiref.sync import sync_to_async
from multiselectfield.db.fields import MSFList

from tgbot.keyboards.timetable_keyboard import set_timetable_for_day_keyboard, set_days_keyboard, timetable_cd, \
    timetable_update_cd
from tgbot.misc.auxiliary_sets import times_lessons_begin, times_breaks, days, lesson_text
from tgbot.misc.parse_StatusOfTheWeek import StatusOfTheWeek
from tgbot.models.timetable import get_timetable_for

logger = logging.getLogger(__name__)


def get_times_for_lesson(lesson_number):
    times_for_lesson = dict()
    time_start = times_lessons_begin[lesson_number]
    time_end = (datetime.strptime(time_start, "%H:%M") + timedelta(hours=1, minutes=25)).strftime("%H:%M")
    time_break = times_breaks[lesson_number]
    times_for_lesson.update(time_start=time_start, time_end=time_end, time_break=time_break)
    return times_for_lesson


async def update_date():
    global date
    date = await StatusOfTheWeek().parse()


async def update_timetable(call: CallbackQuery, **kwargs):
    await update_date()
    status_text = {"1": "нечетную", "2": "четную"}
    status_of_the_week = date.split()[1]
    markup = await set_days_keyboard(status_of_the_week)
    try:
        await call.message.edit_text(
            f"Расписание на <b>{status_text[status_of_the_week]}</b> неделю\n<b>Сегодня</b>: {date}"
        )
        await call.message.edit_reply_markup(markup)
    except Exception as err:
        logger.error(err)
    await call.answer("Успешно обновлено!")


async def set_text_for_timetable(day_of_week, status_of_the_week):
    timetable = await get_timetable_for(day_of_week)
    text_for_timetable = [f"Расписание на день недели <b>{days[day_of_week]}</b>"]
    for lesson in timetable:
        if status_of_the_week in lesson.week_parity:
            for lesson_number in lesson.lesson_number:
                times_for_lesson = get_times_for_lesson(lesson_number)
                text_for_timetable.insert(int(lesson_number), lesson_text.format(
                    lesson_number=lesson_number,
                    subject=lesson.subject.name,
                    type=lesson.type,
                    audience_number=lesson.audience_number,
                    time_start=times_for_lesson['time_start'],
                    time_end=times_for_lesson['time_end'],
                    time_break=times_for_lesson['time_break']
                ))
    if timetable.count() == 0:
        text_for_timetable.append(f"\nЗанятий на день недели <b>{days[day_of_week]}</b> не было добавлено")
    return text_for_timetable


async def show_timetable_menu(message: types.Message):
    await update_date()
    status_of_the_week = date.split()[1]
    await show_list_days(message, status_of_the_week)


async def show_list_days(message: Union[types.Message, types.CallbackQuery], status_of_the_week, **kwargs):
    print(status_of_the_week)
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
        try:
            await call.message.edit_text(
                f"Расписание на <b>{status_text[status_of_the_week]}</b> неделю\n<b>Сегодня</b>: {date}",
                reply_markup=markup
            )
        except Exception as err:
            logger.error(err)


async def show_timetable(call: CallbackQuery, day_of_the_week, status_of_the_week, **kwargs):
    markup = await set_timetable_for_day_keyboard(status_of_the_week)
    await call.answer()
    text_for_timetable = await set_text_for_timetable(day_of_the_week, status_of_the_week)
    await call.message.edit_text(text="\n".join(text_for_timetable), reply_markup=markup)


async def timetable_navigation(call: types.CallbackQuery, callback_data: dict):
    current_level = callback_data.get("level")
    day_of_the_week = callback_data.get("day_of_the_week")
    status_of_the_week = callback_data.get("status_of_the_week")

    levels = {
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


def register_timetable(dp: Dispatcher):
    dp.register_message_handler(show_timetable_menu, commands=["timetable"], state="*")
    dp.register_callback_query_handler(timetable_navigation, timetable_cd.filter(), state="*")
    dp.register_callback_query_handler(update_timetable, timetable_update_cd.filter(), state="*")

