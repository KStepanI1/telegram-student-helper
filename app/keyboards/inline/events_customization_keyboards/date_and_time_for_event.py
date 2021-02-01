from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

get_date_and_time_for_event_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ввести дату", callback_data="get_date_for_event")
        ],
        [
            InlineKeyboardButton(text="Ввести время", callback_data="get_time_for_event")
        ],
        [
            InlineKeyboardButton(text="Как вводить данные", callback_data="how_input_date_and_time")
        ],
        [
            InlineKeyboardButton(text="Сохранить", callback_data="save_date_and_time"),
            InlineKeyboardButton(text="Отмена", callback_data="cancel")
        ]
    ]
)

back_to_date_and_time = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Назад', callback_data="back_to_date_and_time")
        ]
    ]
)


ask_to_save_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Добавить в события", callback_data="add_event_to_events")
        ],
        [
            InlineKeyboardButton(text="Отмена", callback_data="cancel")
        ]
    ]
)
