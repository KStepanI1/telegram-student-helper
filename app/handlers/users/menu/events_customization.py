import datetime
import re
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from app.filters.IsAdmin import IsAdminFilter
from app.keyboards.inline.cancel_keyboard import set_cancel_keyboard
from app.keyboards.inline.events_customization_keyboards.acts_for_edit_events_keyboard import \
    set_acts_for_edit_events_keyboard
from app.keyboards.inline.events_customization_keyboards.date_and_time_for_event import back_to_date_and_time, \
    ask_to_save_keyboard, get_date_and_time_for_event_keyboard
from app.keyboards.inline.events_customization_keyboards.events_list_keyboard import set_events_list_for_remove_keyboard
from app.keyboards.inline.events_customization_keyboards.show_subjects_for_events_edit import \
    set_subjects_for_events_edit_keyboard
from app.loader import dp, bot
from app.states.get_event import GetEvent
from app.utils.db_api.quick_commands.quick_commands_events import add_event, delete_event, select_all_events, \
    get_events, select_event
from app.utils.db_api.quick_commands.quick_commands_subjects import select_all_subjects, select_subject
from app.utils.db_api.quick_commands.quick_commands_user import select_all_users
from app.utils.misc.texts.events_text import how_input_date_and_time_text


async def check_date(date):
    return re.match(
        r"(?:(?:31(\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})",
        date
    )


async def check_time(time):
    return re.match(r"(?:\d\d(:)\d\d)", time)


# function for delete extra zeros from str
def delete_extra_zeros(number: str):
    i = 0
    while number[i] == "0":
        number[i].replace("0", "")
        i += 1


# delete past events from events list
async def delete_past_event():
    events = await select_all_events()
    for event in events:
        now = datetime.datetime.now()
        event_year = event.date.split(".")[2]  # event year number
        event_month = event.date.split(".")[1]  # event month number
        event_day = event.date.split(".")[0]  # event day number
        delete_extra_zeros(event_month)  # delete extra zeros from month number
        delete_extra_zeros(event_day)  # delete extra zeros from day number
        # comparing the current date with the event date
        if (int(event_year) < now.year) or (int(event_day) < now.day and int(event_month) <= now.month) or (
                int(event_month) < now.month):
            await delete_event(event.event_id)


# function of sending to users when adding a new event
async def mailing_when_new_event(subject_name):
    users = await select_all_users()
    for user in users:
        if user.subscription:
            await bot.send_message(chat_id=user.id,
                                   text=f"Добавлено новое событие для предмета <b>{subject_name}</b>")


# ---------------------------------------------
# file events_customization.py:
#
# contains functions for edit events:
# 1. add new event
# 2. delete event
# ---------------------------------------------


@dp.message_handler(Command("event"), IsAdminFilter())
async def show_events_customization_menu(message: Union[types.Message, types.CallbackQuery]):
    subjects = await select_all_subjects()
    if isinstance(message, types.Message):
        await message.answer("Меню событий предметов",
                             reply_markup=set_subjects_for_events_edit_keyboard(subjects=subjects))
    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.answer()
        await call.message.edit_text("Меню событий предметов",
                                     reply_markup=set_subjects_for_events_edit_keyboard(subjects=subjects))


@dp.callback_query_handler(text_contains="select_subject_to_event_edit")
async def show_acts_for_edit_events(call: CallbackQuery):
    await call.answer()
    subject_id = int(call.data.split(":")[-1])
    subject = await select_subject(subject_id)
    await call.message.edit_text(f"Меню события для предмета: <b>{subject.subject_name}</b>",
                                 reply_markup=set_acts_for_edit_events_keyboard(subject_id))


# block "add new event"
# ---------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text_contains="add_new_event")
async def ask_name_new_event(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(date_saved=False)  #
    await state.update_data(time_saved=False)
    subject_id = int(call.data.split(":")[-1])
    subject = await select_subject(subject_id)
    await state.update_data(subject_name=subject.subject_name)
    message_from_bot = await call.message.edit_text(
        f"Введи название события для предмета <b>{subject.subject_name}</b>",
        reply_markup=set_cancel_keyboard)
    # save message_id for delete reply_markup when the user answers
    await state.update_data(message_id=message_from_bot.message_id)
    await GetEvent.GetName.set()


@dp.message_handler(state=GetEvent.GetName)
async def save_name_new_event(message: types.Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get("message_id")
    # delete reply_markup from message with message.message_id == message_id
    await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_id)
    name_new_event = message.text  # message.text == answer from user
    await state.update_data(event_name=name_new_event)
    await message.answer("Имя события успешно сохранено")
    await ask_date_and_time_new_event(message, state)


async def ask_date_and_time_new_event(message: Union[types.Message, types.CallbackQuery], state: FSMContext):
    data = await state.get_data()
    event_name = data.get("event_name")
    if isinstance(message, types.Message):
        await message.answer(f"Введите дату и время для события: <b>{event_name}</b>\n",
                             reply_markup=get_date_and_time_for_event_keyboard)
    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.answer()
        await call.message.edit_text(f"Введите дату и время для события: <b>{event_name}</b>\n",
                                     reply_markup=get_date_and_time_for_event_keyboard)
    await GetEvent.WaitPress.set()


@dp.callback_query_handler(text_contains="get_date_for_event", state=GetEvent.WaitPress)
async def ask_date_for_event(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=10)
    data = await state.get_data()
    event_name = data.get("event_name")
    date_saved = data.get("date_saved")
    # if date was not saved
    if not date_saved:
        await call.message.edit_text(f"Введите дату для события: {event_name}",
                                     reply_markup=set_cancel_keyboard)
        await GetEvent.GetDate.set()
    else:
        await call.message.answer("Вы уже добавили дату для данного события!")


@dp.message_handler(state=GetEvent.GetDate)
async def save_date_for_event(message: types.Message, state: FSMContext):
    date_new_event = message.text
    if await check_date(date_new_event):
        await state.update_data(date_event=date_new_event)
        await state.update_data(date_saved=True)
        await message.answer("Дата события успешно сохранена")
    else:
        await message.answer("Введенная дата неверного формата!\n"
                             "Посмотрите <b>'Как вводить данные'</b> и введите дату заново")
    await ask_date_and_time_new_event(message, state)


@dp.callback_query_handler(text_contains="get_time_for_event", state=GetEvent.WaitPress)
async def ask_time_for_event(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=10)
    data = await state.get_data()
    event_name = data.get("event_name")
    time_saved = data.get("time_saved")
    # if time was not saved
    if not time_saved:
        await call.message.edit_text(f"Введите время для события: {event_name}",
                                     reply_markup=set_cancel_keyboard)
        await GetEvent.GetTime.set()
    else:
        await call.message.answer(text="Вы уже добавили время для данного события!")


@dp.message_handler(state=GetEvent.GetTime)
async def save_time_for_event(message: types.Message, state: FSMContext):
    time_new_event = message.text
    if await check_time(time_new_event):
        await state.update_data(time_event=time_new_event)
        await state.update_data(time_saved=True)
        await message.answer("Время события успешно сохранено")
    else:
        await message.answer("Введенное время неверного формата!\n"
                             "Посмотрите <b>'Как вводить данные'</b> и введите время заново")
    await ask_date_and_time_new_event(message, state)


@dp.callback_query_handler(text_contains="save_date_and_time", state=GetEvent.WaitPress)
async def show_preliminary_result(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    event_name = data.get("event_name")
    date_event = data.get("date_event")
    time_event = data.get("time_event")

    if not date_event:
        await call.message.answer("Поле <b>\"Дата события\"</b> является обязательным!")
    else:
        if not time_event:
            time_event = "-"
            await state.update_data(time_event="-")
        await call.message.edit_text("Хотите сохранить событие?\n"
                                     f"<b>{event_name}</b>  -  Дата: <b>{date_event}</b> Время: <b>{time_event}</b>",
                                     reply_markup=ask_to_save_keyboard)


@dp.callback_query_handler(text_contains="add_event_to_events", state=GetEvent.WaitPress)
async def add_event_to_events(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    subject_name = data.get("subject_name")
    event_name = data.get("event_name")
    date_event = data.get("date_event")
    time_event = data.get("time_event")
    await add_event(subject_name=subject_name, name=event_name, date=date_event, time=time_event)
    await call.message.edit_text(f"Событие для предмета <b>{subject_name}</b> успешно добавлено!")
    await mailing_when_new_event(subject_name)
    await state.finish()


@dp.callback_query_handler(text_contains="how_input_date_and_time", state=GetEvent.WaitPress)
async def show_recommendations(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text=how_input_date_and_time_text, reply_markup=back_to_date_and_time)


@dp.callback_query_handler(text_contains="back_to_date_and_time", state=GetEvent.WaitPress)
async def go_back_to_date_and_time(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await ask_date_and_time_new_event(call, state)


@dp.callback_query_handler(text_contains="cancel", state=GetEvent)
async def cancel_action(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer("Действие отменено!")
    await state.finish()
    await show_events_customization_menu(call.message)


# ---------------------------------------------------------------------------------------------------------------------


# block "delete event"
# ---------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text_contains="delete_event")
async def show_events_list_for_choice(call: CallbackQuery):
    await call.answer()
    subject_id = int(call.data.split(":")[-1])
    subject = await select_subject(subject_id)
    events = await get_events(subject.subject_name)
    markup = await set_events_list_for_remove_keyboard(events)
    await call.message.edit_text("Выберите событие для удаления", reply_markup=markup)


@dp.callback_query_handler(text_contains="select_event_for_remove")
async def remove_selected_event(call: CallbackQuery, state: FSMContext):
    await call.answer()
    event_id = int(call.data.split(":")[-1])
    event = await select_event(event_id)
    await delete_event(event_id)
    await call.message.edit_text(f"Событие <b>{event.subject_name}</b> :  <b>{event.name}</b> успешно удалено")
    await state.finish()
    await show_events_customization_menu(call.message)


# ---------------------------------------------------------------------------------------------------------------------


@dp.callback_query_handler(text_contains="back_to_events")
async def go_back_to_events(call: CallbackQuery):
    await call.answer()
    await show_events_customization_menu(call)


@dp.callback_query_handler(text_contains="finish_add_or_edit_events")
async def finish_add_or_edit_events(call: CallbackQuery):
    await call.answer()
    await bot.delete_message(call.message.chat.id, call.message.message_id)
