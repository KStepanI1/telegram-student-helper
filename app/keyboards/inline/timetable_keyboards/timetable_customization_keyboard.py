from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from app.utils.misc.texts.timetable import classes, days, statuses_of_the_week

timetable_edit_cd = CallbackData("show_timetable", "level", "day_of_the_week", "couple_number",
                                 "status", "edit_choice")


def make_callback_data(level, day_of_the_week="0", couple_number="0", status="0", edit_choice="0"):
    return timetable_edit_cd.new(level=level, day_of_the_week=day_of_the_week, couple_number=couple_number,
                                 status=status, edit_choice=edit_choice)


async def set_days_for_edit_keyboard():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup()

    for day in days:
        button_text = f"{days[day]}"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           day_of_the_week=day)
        markup.row(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    markup.row(
        InlineKeyboardButton(text="Закрыть", callback_data=make_callback_data(level=-1))
    )

    return markup


async def set_couples_keyboard(day_of_the_week):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup()

    for couple in classes:
        button_text = f"{couple}"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           day_of_the_week=day_of_the_week,
                                           couple_number=couple)
        markup.row(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=make_callback_data(level=CURRENT_LEVEL - 1))
    )

    return markup


async def set_status_of_the_week_keyboard(day_of_the_week, couple, edit_choice):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup()

    for status in statuses_of_the_week:
        button_text = f"{status}"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           day_of_the_week=day_of_the_week,
                                           couple_number=couple,
                                           edit_choice=edit_choice,
                                           status=statuses_of_the_week[status]
                                           )
        markup.row(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                                                            day_of_the_week=day_of_the_week,
                                                                            couple_number=couple))
    )
    return markup


async def set_acts_for_edit_keyboard(day_of_the_week, couple):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup()

    button_text = f"Добавить / Изменить"
    callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                       day_of_the_week=day_of_the_week,
                                       couple_number=couple,
                                       edit_choice="edit_couple_name")
    markup.row(
        InlineKeyboardButton(text=button_text, callback_data=callback_data)
    )
    button_text = f"Удалить"
    callback_data = make_callback_data(level=CURRENT_LEVEL + 2,
                                       day_of_the_week=day_of_the_week,
                                       couple_number=couple,
                                       edit_choice="delete_couple")
    markup.row(
        InlineKeyboardButton(text=button_text, callback_data=callback_data)
    )

    markup.row(
        InlineKeyboardButton(text="К выбору пары",
                             callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                                              day_of_the_week=day_of_the_week))
    )

    return markup


async def set_cancel_keyboard():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Отмена", callback_data=make_callback_data(level=0))]]
    )
    return markup
