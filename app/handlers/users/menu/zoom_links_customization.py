from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from app.filters.IsAdmin import IsAdminFilter
from app.keyboards.inline.zoom_links_keyboard import show_subjects_for_links_edit, add_or_remove_links
from app.loader import dp
from app.utils.db_api.quick_commands.quick_commands_subjects import select_all_subjects, select_subject


@dp.message_handler(Command("zoom"), IsAdminFilter())
async def show_subjects_for_link_edit(message: types.Message):
    subjects = await select_all_subjects()
    await message.answer("Меню редактирования ZOOM ссылок",
                         reply_markup=show_subjects_for_links_edit(subjects))


@dp.callback_query_handler(text_contains="select_subject_to_link_edit")
async def show_acts_with_links(call: CallbackQuery):
    await call.answer(cache_time=60)
    subject_id = call.data.split(":")[-1]
    subject = await select_subject(subject_id=subject_id)
    await call.message.answer(f"Меню редактирования ZOOM ссылок для предмета: <b>{subject}</b>",
                              reply_markup=add_or_remove_links(subject_id=subject_id))


@dp.callback_query_handler(text_contains="add_link")
async def show_links_edit_menu(call: CallbackQuery):
    await call.answer(cache_time=60)
