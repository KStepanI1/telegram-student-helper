from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def set_subjects_for_events_edit_keyboard(subjects):
    keyboards = []
    for subject in subjects:
        keyboard = [InlineKeyboardButton(text=f"{subject.subject_name}",
                                         callback_data=f"select_subject_to_event_edit:{subject.subject_id}")]
        keyboards.append(keyboard)
    keyboard = [InlineKeyboardButton(text=f"Закрыть", callback_data=f"finish_add_or_edit_events")]
    keyboards.append(keyboard)
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)
    return keyboard
