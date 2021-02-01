from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from app.filters.IsAdmin import IsAdminFilter
from app.keyboards.inline.cancel_keyboard import set_cancel_keyboard
from app.keyboards.inline.subjects_customization_keyboards.edit_subject_keyboard import edit_subject_keyboard
from app.keyboards.inline.subjects_customization_keyboards.show_subjects_for_subjects_edit import \
    set_subjects_list_keyboard
from app.loader import dp, bot
from app.utils.db_api.quick_commands.quick_commands_subjects import add_subject, delete_subject, \
    select_subject, select_all_subjects
from app.utils.db_api.quick_commands.quick_commands_zoom import add_link


@dp.message_handler(Command("subject"), IsAdminFilter())
async def show_subjects_customization_menu(message: Union[types.Message, types.CallbackQuery]):
    subjects = await select_all_subjects()
    if isinstance(message, types.Message):
        await message.answer("Меню действий с предметами", reply_markup=set_subjects_list_keyboard(subjects))
    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.answer()
        await call.message.edit_text(text="Меню действий с предметами",
                                     reply_markup=set_subjects_list_keyboard(subjects))


@dp.callback_query_handler(text_contains="add_new_subject")
async def ask_name_new_subject(call: CallbackQuery, state: FSMContext):
    message_from_bot = await call.message.edit_text(text="Введи название предмета",
                                                    reply_markup=set_cancel_keyboard)
    await state.update_data(message_id=message_from_bot.message_id)
    await state.set_state("name_new_subject")


@dp.message_handler(state="name_new_subject")
async def add_new_subject(message: types.Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get("message_id")
    await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_id)
    await add_subject(subject_name=message.text)
    await add_link(subject_name=message.text)
    await state.finish()
    await message.answer("Предмет успешно добавлен!")
    await show_subjects_customization_menu(message)


@dp.callback_query_handler(text_contains="cancel", state="name_new_subject")
async def cancel_action(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer("Добавление отменено!")


@dp.callback_query_handler(text_contains="select_subject_to_edit")
async def show_submenu_to_selected_subject(call: CallbackQuery):
    await call.answer(cache_time=60)
    subject_id = int(call.data.split(":")[-1])
    subject = await select_subject(subject_id)
    await call.message.edit_text(text=f"Меню редактирования предмета: {subject.subject_name}",
                                 reply_markup=edit_subject_keyboard(subject.subject_id))


@dp.callback_query_handler(text_contains="delete_subject")
async def remove_subject(call: CallbackQuery):
    await call.answer(cache_time=60)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    subject_id = int(call.data.split(":")[-1])
    await delete_subject(subject_id=subject_id)
    await call.message.answer("Предмет успешно удален!")
    await show_subjects_customization_menu(call.message)


@dp.callback_query_handler(text_contains="back_to_subjects")
async def go_back_to_subjects(call: CallbackQuery):
    await call.answer(cache_time=60)
    await show_subjects_customization_menu(call)


@dp.callback_query_handler(text_contains="finish_add_or_edit_subjects")
async def finish_show_subjects(call: CallbackQuery):
    await call.answer(cache_time=60)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
