from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from app.utils.db_api.quick_commands.quick_commands_subjects import select_all_subjects

menu_cd = CallbackData("show_menu", "level", "subject_name", "subcategory_id", "subject_id")


def make_callback_data(level, subject_name="-", subject_id="0", subcategory_id=0):
    return menu_cd.new(level=level, subject_name=subject_name, subject_id=subject_id, subcategory_id=subcategory_id)


async def set_subject_categories_keyboard():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup()

    subjects = await select_all_subjects()
    for subject in subjects:
        button_text = f"{subject.subject_name}"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, subject_name=subject.subject_name,
                                           subject_id=subject.subject_id)
        markup.row(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    markup.row(
        InlineKeyboardButton(text="Закрыть", callback_data=make_callback_data(level=-1))
    )

    return markup


async def set_subject_subcategories_keyboard(subject_id, subject_name):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup()

    subcategories = ["ZOOM ссылки", "Ближайшие события", "Преподаватели"]
    subcategory_id = 1
    for subcategory in subcategories:
        button_text = f"{subcategory}"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, subject_id=subject_id,
                                           subcategory_id=subcategory_id, subject_name=subject_name)
        markup.row(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
        subcategory_id += 1
    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=make_callback_data(CURRENT_LEVEL - 1))
    )

    return markup


async def set_subcategory_keyboard(subject_id, subject_name):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup()

    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                                                            subject_id=subject_id,
                                                                            subject_name=subject_name))
    )

    return markup
