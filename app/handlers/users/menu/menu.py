from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from app.keyboards.inline.menu_keyboards.menu_keyboard import set_subject_categories_keyboard, \
    set_subject_subcategories_keyboard, \
    menu_cd, set_subcategory_keyboard
from app.loader import dp, bot
from app.utils.db_api.quick_commands.quick_commands_events import get_events
from app.utils.db_api.quick_commands.quick_commands_teachers import get_teachers
from app.utils.db_api.quick_commands.quick_commands_zoom import select_link
from app.utils.misc import rate_limit
from app.utils.misc.texts.events_text import events_title_text, event_text
from app.utils.misc.texts.teacher_text import teacher_text
from app.utils.misc.texts.timetable import set_timetable
from app.utils.misc.texts.zoom_link_text import zoom_link


async def link_processing(link):
    if not link.lectures_code:
        link.lectures_code = "Отсутствует"
    if not link.lectures_password:
        link.lectures_password = "Отсутствует"
    if not link.lectures_link:
        link.lectures_link = "Отсутствует"
    if not link.practices_code:
        link.practices_code = "Отсутствует"
    if not link.practices_password:
        link.practices_password = "Отсутствует"
    if not link.practices_link:
        link.practices_link = "Отсутствует"


@rate_limit(5, 'menu')
@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    await show_subject_categories(message)


async def show_subject_categories(message: Union[types.Message, types.CallbackQuery], **kwargs):
    markup = await set_subject_categories_keyboard()

    if isinstance(message, types.Message):
        await message.answer("<b>Меню учебных предметов</b>", reply_markup=markup)

    elif isinstance(message, types.CallbackQuery):
        callback = message
        await callback.answer()
        await callback.message.edit_text(text="<b>Меню учебных предметов</b>", reply_markup=markup)


async def show_subject_subcategories(callback: CallbackQuery, subject_name, subject_id, **kwargs):
    await callback.answer()
    markup = await set_subject_subcategories_keyboard(subject_id, subject_name)
    await callback.message.edit_text(text=f"Меню предмета: <b>{subject_name}</b>",
                                     reply_markup=markup)


async def show_subcategory(callback: CallbackQuery, subcategory_id, subject_name, subject_id, **kwargs):
    await callback.answer()
    markup = await set_subcategory_keyboard(subject_id=subject_id, subject_name=subject_name)
    if subcategory_id == 1:
        await show_links(subject_name, callback, markup)
    elif subcategory_id == 2:
        await show_events(subject_name, callback, markup)
    elif subcategory_id == 3:
        await show_teachers(subject_name, callback, markup)


async def finish_menu(callback: CallbackQuery, **kwargs):
    await callback.answer()
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)


@dp.callback_query_handler(menu_cd.filter())
async def menu_navigation(call: types.CallbackQuery, callback_data: dict):
    current_level = callback_data.get("level")
    subject_id = int(callback_data.get("subject_id"))
    subject_name = callback_data.get("subject_name")
    subcategory_id = int(callback_data.get("subcategory_id"))

    levels = {
        "-1": finish_menu,
        "0": show_subject_categories,
        "1": show_subject_subcategories,
        "2": show_subcategory
    }
    current_level_function = levels[current_level]

    await current_level_function(
        call,
        subject_id=subject_id,
        subject_name=subject_name,
        subcategory_id=subcategory_id
    )


async def show_links(subject_name, callback, markup):
    link = await select_link(subject_name)
    await link_processing(link)
    await callback.message.edit_text(text=zoom_link.format(
        subject_name=link.subject_name,
        lectures_code=link.lectures_code,
        lectures_password=link.lectures_password,
        lectures_link=link.lectures_link,
        practices_code=link.practices_code,
        practices_password=link.practices_password,
        practices_link=link.practices_link
    ), reply_markup=markup)


async def show_events(subject_name, callback, markup):
    all_events_text = [events_title_text.format(subject=subject_name)]
    events = await get_events(subject_name)
    if events:
        number = 0
        for event in events:
            number += 1
            event = event_text.format(number=number, event_name=event.name,
                                      event_date=event.date, event_time=event.time)
            all_events_text.append(event)
    else:
        all_events_text.append("Событий по данному предмету не было добавлено\n")
    await callback.message.edit_text("\n".join(all_events_text), reply_markup=markup)


async def show_teachers(subject_name, callback, markup):
    teachers = await get_teachers(subject_name)
    all_teachers_text = [f"Преподаватели по предмету <b>{subject_name}</b>"]
    if teachers:
        number = 0
        for teacher in teachers:
            number += 1
            teacher = teacher_text.format(
                number=number,
                teacher_name=teacher.teacher_name,
                kind_of_activity=teacher.kind_of_activity,
                teacher_mail=teacher.teacher_mail,
            )
            all_teachers_text.append(teacher)
    else:
        all_teachers_text.append("\nПреподавателей по данному предмету не было добавлено")
    await callback.message.edit_text("\n".join(all_teachers_text), reply_markup=markup)
