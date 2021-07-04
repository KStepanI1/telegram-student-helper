from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.misc.auxiliary_sets import days

timetable_cd = CallbackData("show_timetable", "level", "day_of_the_week", "status_of_the_week")
timetable_update_cd = CallbackData("update_timetable", "status_of_the_week")


def make_timetable_update_cd(status_of_the_week):
    return timetable_update_cd.new(status_of_the_week=status_of_the_week)


def make_timetable_cd(level, day_of_the_week="0", status_of_the_week="0"):
    return timetable_cd.new(level=level, day_of_the_week=day_of_the_week, status_of_the_week=status_of_the_week)


async def set_days_keyboard(status_of_the_week):
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup()

    for day in days:
        button_text = f"{days[day]}"
        callback_data = make_timetable_cd(level=CURRENT_LEVEL + 1,
                                          day_of_the_week=day,
                                          status_of_the_week=status_of_the_week)
        markup.row(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    reverse_status = {"1": "2", "2": "1"}
    status_text = {"1": "Четная", "2": "Нечетная"}
    button_text = f"{status_text[status_of_the_week]} неделя"
    callback_data = make_timetable_cd(level=CURRENT_LEVEL, status_of_the_week=reverse_status[status_of_the_week])
    markup.row(
        InlineKeyboardButton(text=button_text, callback_data=callback_data),
        InlineKeyboardButton(text="Обновить",
                             callback_data=make_timetable_update_cd(status_of_the_week=status_of_the_week))
    )

    return markup


async def set_timetable_for_day_keyboard(status_of_the_week):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup()

    markup.row(
        InlineKeyboardButton(text="Назад",
                             callback_data=make_timetable_cd(level=CURRENT_LEVEL - 1,
                                                             status_of_the_week=status_of_the_week))
    )

    return markup
