from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.utils.db_api.quick_commands.quick_commands_subjects import select_all_subjects


def set_subjects_list_keyboard(subjects):
    keyboards = []
    for subject in subjects:
        keyboard = [InlineKeyboardButton(text=f"{subject.subject_name}",
                                         callback_data=f"select_subject_to_edit:{subject.subject_id}")]
        keyboards.append(keyboard)
    keyboard = [InlineKeyboardButton(text=f"Добавить новый", callback_data="add_new_subject")]
    keyboards.append(keyboard)
    keyboard = [InlineKeyboardButton(text=f"Закрыть", callback_data=f"finish_add_or_edit_subjects")]
    keyboards.append(keyboard)
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)
    return keyboard
