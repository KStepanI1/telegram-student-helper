from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from app.utils.db_api.quick_commands.quick_commands_subjects import select_all_subjects, select_subject
from app.utils.db_api.quick_commands.quick_commands_teachers import get_teachers

teachers_customization_cd = CallbackData("show", "level", "subject_id", "action", "teacher_id")


def make_callback_data(level, subject_id="0", action="0", teacher_id="0"):
    return teachers_customization_cd.new(level=level, subject_id=subject_id, action=action, teacher_id=teacher_id)


async def set_subjects_keyboard():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup()

    subjects = await select_all_subjects()
    for subject in subjects:
        button_text = f"{subject.subject_name}"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, subject_id=subject.subject_id)
        markup.row(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    markup.row(
        InlineKeyboardButton(text="Закрыть", callback_data=make_callback_data(level=-1))
    )

    return markup


async def set_acts_teachers_edit_keyboard(subject_id):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup()

    button_text = f"Добавить"
    callback_data = make_callback_data(level=CURRENT_LEVEL + 2, subject_id=subject_id, action="add_teacher")
    markup.row(
        InlineKeyboardButton(text=button_text, callback_data=callback_data)
    )
    button_text = f"Изменить"
    callback_data = make_callback_data(level=CURRENT_LEVEL + 1, subject_id=subject_id, action="edit_teacher")
    markup.row(
        InlineKeyboardButton(text=button_text, callback_data=callback_data)
    )
    button_text = f"Удалить"
    callback_data = make_callback_data(level=CURRENT_LEVEL + 1, subject_id=subject_id, action="delete_teacher")
    markup.row(
        InlineKeyboardButton(text=button_text, callback_data=callback_data)
    )

    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=make_callback_data(level=CURRENT_LEVEL - 1))
    )

    return markup


async def set_teachers_list_keyboard(subject_id, action):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup()
    subject = await select_subject(int(subject_id))
    teachers = await get_teachers(subject_name=subject.subject_name)
    for teacher in teachers:
        button_text = f"{teacher.teacher_name}"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, subject_id=subject_id, action=action,
                                           teacher_id=teacher.teacher_id)
        markup.row(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(text="Назад",
                             callback_data=make_callback_data(level=CURRENT_LEVEL - 1, subject_id=subject_id))
    )
    return markup


async def set_acts_for_edit_selected_teacher_keyboard(subject_id, action):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text="Изменить ФИО",
                             callback_data="edit_fio"
                             )
    )
    markup.row(
        InlineKeyboardButton(text="Изменить почту",
                             callback_data="edit_mail")
    )
    markup.row(
        InlineKeyboardButton(text="Назад",
                             callback_data=make_callback_data(level=CURRENT_LEVEL - 1, subject_id=subject_id,
                                                              action=action))
    )
    return markup


async def set_cancel_action_keyboard():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Отмена", callback_data="teacher_customization_action_cancel")
            ]
        ]
    )
    return markup
