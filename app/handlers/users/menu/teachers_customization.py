import re
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from app.filters.IsAdmin import IsAdminFilter
from app.keyboards.inline.teachers_customization_keyboard import set_subjects_keyboard, set_acts_teachers_edit_keyboard, \
    set_teachers_list_keyboard, teachers_customization_cd, set_cancel_action_keyboard, \
    set_acts_for_edit_selected_teacher_keyboard
from app.loader import dp, bot
from app.states.teachers import EditTeacher, GetTeacher
from app.utils.db_api.quick_commands import quick_commands_teachers
from app.utils.db_api.quick_commands.quick_commands_subjects import select_subject
from app.utils.db_api.quick_commands.quick_commands_teachers import update_teacher_name, \
    select_teacher, delete_teacher, update_teacher_mail


async def check_mail(mail):
    return re.match(r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+", mail) or mail == "Отсутствует"


@dp.message_handler(Command("teacher"), IsAdminFilter())
async def show_teachers_customization_menu(message: types.Message):
    await show_subjects_list(message)


async def show_subjects_list(message: Union[types.Message, types.CallbackQuery], **kwargs):
    markup = await set_subjects_keyboard()

    if isinstance(message, types.Message):
        await message.answer("Меню редактирования информации о преподавателях",
                             reply_markup=markup)
    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.answer()
        await call.message.edit_text("Меню редактирования информации о преподавателях",
                                     reply_markup=markup)


async def show_acts_for_teachers_edit(callback: CallbackQuery, subject_id, **kwargs):
    await callback.answer()
    markup = await set_acts_teachers_edit_keyboard(subject_id)

    await callback.message.edit_text(text="Выберите действие",
                                     reply_markup=markup)


async def show_teachers_list(callback: CallbackQuery, subject_id, action, **kwargs):
    await callback.answer()
    markup = await set_teachers_list_keyboard(subject_id, action)
    subject = await select_subject(subject_id)
    await callback.message.edit_text(text=f"Выберите преподавателя по предмету: <b>{subject.subject_name}</b>",
                                     reply_markup=markup)


async def performing_the_selected_action(callback: CallbackQuery, state, action, teacher_id, subject_id,
                                         **kwargs):
    await callback.answer()
    markup = await set_cancel_action_keyboard()

    if action == 'add_teacher':
        await ask_name_new_teacher(callback, state, subject_id, markup)

    elif action == 'edit_teacher':
        await show_acts_for_teacher_edit(callback, state, subject_id, action, teacher_id)

    elif action == "delete_teacher":
        await delete_selected_teacher(callback, teacher_id)


async def finish_teachers_customization_menu(callback: CallbackQuery, state, **kwargs):
    await callback.answer()
    await bot.delete_message(chat_id=callback.message.chat.id,
                             message_id=callback.message.message_id)
    await state.finish()


@dp.callback_query_handler(teachers_customization_cd.filter(), state="*")
async def teachers_customization_navigation(call: CallbackQuery, state: FSMContext, callback_data: dict):
    current_level = callback_data.get("level")
    subject_id = int(callback_data.get("subject_id"))
    teacher_id = int(callback_data.get("teacher_id"))
    action = callback_data.get("action")

    levels = {
        "-1": finish_teachers_customization_menu,
        "0": show_subjects_list,
        "1": show_acts_for_teachers_edit,
        "2": show_teachers_list,
        "3": performing_the_selected_action,
    }
    current_level_function = levels[current_level]

    await current_level_function(
        call,
        subject_id=subject_id,
        action=action,
        teacher_id=teacher_id,
        state=state,
    )


async def ask_name_new_teacher(call: CallbackQuery, state: FSMContext, subject_id, markup):
    await call.answer()
    message_from_bot = await call.message.edit_text("Введите ФИО преподавателя",
                                                    reply_markup=markup)
    await state.update_data(subject_id=subject_id)
    await state.update_data(message_id=message_from_bot.message_id)
    await GetTeacher.GetName.set()


@dp.message_handler(state=GetTeacher.GetName)
async def ask_teacher_mail(message: types.Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get("message_id")
    if message_id:
        await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_id)
    await state.update_data(teacher_name=message.text)
    markup = await set_cancel_action_keyboard()
    message_from_bot = await message.answer("Введите электронную почту преподавателя\n"
                                            "Если почта отстуствует, введите 'Отсутствует' "
                                            "<b>(с большой буквы обязательно!)</b>",
                                            reply_markup=markup)
    await state.update_data(message_id=message_from_bot.message_id)
    await GetTeacher.GetMail.set()


@dp.message_handler(state=GetTeacher.GetMail)
async def ask_kind_of_teacher_activity(message: types.Message, state: FSMContext):
    teacher_mail = message.text
    if await check_mail(teacher_mail):
        data = await state.get_data()
        message_id = data.get("message_id")
        await state.update_data(teacher_mail=message.text)
        await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_id)
        markup = await set_cancel_action_keyboard()
        message_from_bot = await message.answer("Введите вид деятельности преподавателя (Лекции, Практики, Семинары)",
                                                reply_markup=markup)
        await state.update_data(message_id=message_from_bot.message_id)
        await GetTeacher.GetKind.set()
    else:
        await message.answer("Введенная почта некорректна. Повторите попытку")
        await ask_teacher_mail(message, state)


@dp.message_handler(state=GetTeacher.GetKind)
async def add_new_teacher(message: types.Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get("message_id")
    subject_id = data.get("subject_id")
    teacher_name = data.get("teacher_name")
    teacher_mail = data.get("teacher_mail")
    kind_of_activity = message.text
    await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_id)
    subject = await select_subject(subject_id)
    await quick_commands_teachers.add_teacher(teacher_name=teacher_name,
                                              teacher_mail=teacher_mail,
                                              kind_of_activity=kind_of_activity,
                                              subject_name=subject.subject_name)
    await state.finish()
    await message.answer(
        f"Преподаватель <b>{teacher_name}</b> : <b>{teacher_mail}</b> : <b>{kind_of_activity}</b> "
        f"был успешно добавлен в список учителей")
    await show_teachers_customization_menu(message)


async def show_acts_for_teacher_edit(call, state, subject_id, action, teacher_id):
    await call.answer()
    await state.update_data(teacher_id=teacher_id)
    markup = await set_acts_for_edit_selected_teacher_keyboard(subject_id, action)
    await call.message.edit_text("Выберите что хотите изменить",
                                 reply_markup=markup)


@dp.callback_query_handler(text_contains="edit_fio")
async def ask_new_teacher_fio(call: CallbackQuery, state: FSMContext):
    await call.answer()
    markup = await set_cancel_action_keyboard()
    message_from_bot = await call.message.edit_text("Введите новое ФИО преподавателя",
                                                    reply_markup=markup)
    await state.update_data(message_id=message_from_bot.message_id)
    await EditTeacher.EditName.set()


@dp.message_handler(state=EditTeacher.EditName)
async def save_new_teacher_fio(message: types.Message, state: FSMContext):
    new_teacher_name = message.text
    data = await state.get_data()
    message_id = data.get("message_id")
    teacher_id = data.get("teacher_id")
    await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_id)
    teacher = await select_teacher(teacher_id)
    old_teacher_name = teacher.teacher_name
    await update_teacher_name(teacher_id, new_teacher_name)
    await state.finish()
    await message.answer(
        f"ФИО преподавателя успешно изменено:\n"
        f"c <b>{old_teacher_name}</b>\n"
        f"на <b>{new_teacher_name}</b>")
    await show_teachers_customization_menu(message)


@dp.callback_query_handler(text_contains="edit_mail")
async def ask_new_teacher_mail(message: Union[types.Message, types.CallbackQuery], state: FSMContext):
    markup = await set_cancel_action_keyboard()
    if isinstance(message, types.Message):
        message_from_bot = await message.answer("Введите новую почту преподавателя"
                                                "Если почта отстуствует, введите 'Отсутствует'"
                                                "<b>(с большой буквы обязательно!)</b>",
                                                reply_markup=markup)
        await state.update_data(message_id=message_from_bot.message_id)
    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.answer()
        message_from_bot = await call.message.edit_text("Введите новую почту преподавателя"
                                                        "Если почта отстуствует, введите 'Отсутствует'"
                                                        "<b>(с большой буквы обязательно!)</b>",
                                                        reply_markup=markup)
        await state.update_data(message_id=message_from_bot.message_id)
    await EditTeacher.EditMail.set()


@dp.message_handler(state=EditTeacher.EditMail)
async def save_new_teacher_mail(message: types.Message, state: FSMContext):
    new_teacher_mail = message.text
    if await check_mail(new_teacher_mail):
        data = await state.get_data()
        message_id = data.get("message_id")
        teacher_id = data.get("teacher_id")
        await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_id)
        teacher = await select_teacher(teacher_id)
        old_teacher_mail = teacher.teacher_mail
        await update_teacher_mail(teacher_id, new_teacher_mail)
        await state.finish()
        await message.answer(
            f"ФИО преподавателя успешно изменено:\n"
            f"c <b>{old_teacher_mail}</b>\n"
            f"на <b>{new_teacher_mail}</b>")
        await show_teachers_customization_menu(message)
    else:
        await message.answer("Введенная почта некорректна. Повторите попытку")
        await ask_new_teacher_mail(message, state)


async def delete_selected_teacher(call: CallbackQuery, teacher_id):
    teacher = await select_teacher(teacher_id)
    await call.answer()
    await delete_teacher(teacher_id)
    await call.message.edit_text(f"Преподаватель <b>{teacher.teacher_name}</b> был успешно удален из списка учителей")
    await show_teachers_customization_menu(call.message)


@dp.callback_query_handler(text_contains="teacher_customization_action_cancel", state="*")
async def cancel_action(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.finish()
    await show_subjects_list(call)
