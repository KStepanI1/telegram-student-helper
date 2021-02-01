from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def set_events_list_for_remove_keyboard(events):
    markup = InlineKeyboardMarkup()
    for event in events:
        button_text = f"{event.subject_name} :  {event.name} :   {event.date}   {event.time}"
        callback_data = f"select_event_for_remove:{event.event_id}"
        markup.row(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(text="Назад", callback_data="back_to_acts_for_edit_events")
    )
    return markup
