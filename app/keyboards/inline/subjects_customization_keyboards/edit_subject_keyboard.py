from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def edit_subject_keyboard(subject):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Удалить", callback_data=f"delete_subject:{subject}")
            ],
            [
                InlineKeyboardButton(text="Назад", callback_data="back_to_subjects")
            ]
        ]
    )
    return keyboard
