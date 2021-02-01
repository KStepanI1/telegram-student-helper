from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

set_cancel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Отмена", callback_data="cancel")
        ]
    ]
)