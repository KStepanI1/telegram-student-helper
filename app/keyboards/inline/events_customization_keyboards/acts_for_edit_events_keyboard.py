from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def set_acts_for_edit_events_keyboard(subject_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Добавить", callback_data=f"add_new_event:{subject_id}")
            ],
            [
                InlineKeyboardButton(text="Удалить", callback_data=f"delete_event:{subject_id}")
            ],
            [
                InlineKeyboardButton(text="Назад", callback_data="back_to_events")
            ]
        ]
    )
    return keyboard
