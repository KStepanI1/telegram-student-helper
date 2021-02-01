from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def show_subjects_for_links_edit(subjects):
    keyboards = []
    for subject in subjects:
        keyboard = [InlineKeyboardButton(text=f"{subject.subject}",
                                         callback_data=f"select_subject_to_link_edit:{subject.subject_id}")]
        keyboards.append(keyboard)
    keyboard = [InlineKeyboardButton(text=f"Закрыть", callback_data=f"finish_add_or_remove_links")]
    keyboards.append(keyboard)
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)
    return keyboard


def add_or_remove_links(subject_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Добавить ссылку(и)", callback_data=f"add_link:{subject_id}")
            ],
            [
                InlineKeyboardButton(text="Удалить ссылку(и)", callback_data=f"delete_link:{subject_id}")
            ],
            [
                InlineKeyboardButton(text="Назад", callback_data="back_to_links")
            ]
        ]
    )
    return keyboard
