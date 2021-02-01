from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from app.filters.IsAdmin import IsAdminFilter
from app.keyboards.inline.timetable_keyboards.timetable_customization_keyboard import timetable_edit_cd, \
    set_days_for_edit_keyboard, \
    set_couples_keyboard, set_status_of_the_week_keyboard, set_acts_for_edit_keyboard, set_cancel_keyboard
from app.loader import dp, bot
from app.states.get_couple import GetCouple
from app.utils.db_api.quick_commands.quick_commands_timetable import edit_couple_name_even, edit_couple_name_odd, \
    delete_couple_name_even, delete_couple_name_odd
from app.utils.misc.texts.timetable import days, reverse_classes


@dp.message_handler(Command("timetable_edit"), IsAdminFilter())
async def show_timetable_customization_menu(message: types.Message):
    await show_list_days(message)


async def show_list_days(message: Union[types.Message, types.CallbackQuery], **kwargs):
    markup = await set_days_for_edit_keyboard()

    if isinstance(message, types.Message):
        await message.answer(f"<b>Редактирование расписания</b>", reply_markup=markup)

    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.answer()
        await call.message.edit_text(f"<b>Редактирование расписания</b>",
                                     reply_markup=markup)


async def show_list_couples(call: CallbackQuery, day_of_the_week, **kwargs):
    markup = await set_couples_keyboard(day_of_the_week)
    await call.answer()
    await call.message.edit_text(text=f"<b>{days[day_of_the_week]}</b>\n"
                                      "Выберите нужную пару", reply_markup=markup)


async def get_status_of_the_week(call: CallbackQuery, day_of_the_week, couple, edit_choice, **kwargs):
    markup = await set_status_of_the_week_keyboard(day_of_the_week=day_of_the_week,
                                                   couple=couple, edit_choice=edit_choice)
    await call.answer()
    await call.message.edit_text(text=f"<b>{days[day_of_the_week]}</b> :  <b>{reverse_classes[couple]}</b>\n"
                                      "Выберите <b>статус</b> пары", reply_markup=markup)


async def show_list_acts_for_edit(call: CallbackQuery, day_of_the_week, couple, **kwargs):
    markup = await set_acts_for_edit_keyboard(day_of_the_week=day_of_the_week, couple=couple)
    await call.answer()
    await call.message.edit_text(
        text=f"<b>{days[day_of_the_week]}</b> :  <b>{reverse_classes[couple]}</b>\n"
             "Выберите действие", reply_markup=markup)


async def acts_execute(call: CallbackQuery, state, day_of_the_week, couple, edit_choice, status, **kwargs):
    markup = await set_cancel_keyboard()
    await call.answer()
    await state.update_data(day_of_the_week=day_of_the_week)
    await state.update_data(couple=couple)
    if edit_choice == "edit_couple_name":
        message_from_bot = await call.message.edit_text("Введите название пары и вертикальной чертой"
                                                        "<b>отделите номер аудиториии</b>", reply_markup=markup)
        await state.update_data(message_id=message_from_bot.message_id)
        if status == "even":
            await GetCouple.GetEvenCouple.set()
        elif status == "odd":
            await GetCouple.GetOddCouple.set()
        elif status == "not_change":
            await GetCouple.GetNotChangeCouple.set()
    elif edit_choice == "delete_couple":
        await delete_couple_name_even(day_of_the_week + str(couple))
        await delete_couple_name_odd(day_of_the_week + str(couple))
        await call.message.edit_text("Пара успешно удалена")


@dp.callback_query_handler(state=GetCouple)
async def cancel_action(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer()
    await show_list_days(call)


async def finish_timetable_edit(call: CallbackQuery, state, **kwargs):
    await bot.delete_message(call.message.chat.id, call.message.message_id)


@dp.callback_query_handler(timetable_edit_cd.filter())
async def timetable_customization_menu_navigation(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    current_level = callback_data.get("level")
    day_of_the_week = callback_data.get("day_of_the_week")
    couple_number = int(callback_data.get("couple_number").split()[-1])
    edit_choice = callback_data.get("edit_choice")
    status = callback_data.get("status")

    levels = {
        "-1": finish_timetable_edit,
        "0": show_list_days,
        "1": show_list_couples,
        "2": show_list_acts_for_edit,
        "3": get_status_of_the_week,
        "4": acts_execute
    }
    current_level_function = levels[current_level]

    await current_level_function(
        call,
        level=current_level,
        day_of_the_week=day_of_the_week,
        couple=couple_number,
        edit_choice=edit_choice,
        status=status,
        state=state,
    )


@dp.message_handler(state=GetCouple.GetEvenCouple)
async def ask_audience_number(message: types.Message, state: FSMContext):
    callback_data = await state.get_data()
    message_id = callback_data.get("message_id")
    day_of_the_week = callback_data.get("day_of_the_week")
    couple = callback_data.get("couple")
    await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_id)
    await edit_couple_name_even(day_of_the_week + str(couple), message.text)
    await message.answer(f"Название пары <b>{days[day_of_the_week]}</b> :  {reverse_classes[couple]} "
                         f"<b>для четной недели</b> успешно изменено!")
    await state.finish()
    await show_timetable_customization_menu(message)


@dp.message_handler(state=GetCouple.GetOddCouple)
async def ask_audience_number(message: types.Message, state: FSMContext):
    callback_data = await state.get_data()
    message_id = callback_data.get("message_id")
    day_of_the_week = callback_data.get("day_of_the_week")
    couple = callback_data.get("couple")
    await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_id)
    await edit_couple_name_odd(day_of_the_week + str(couple), message.text)
    await message.answer(f"Название пары <b>{days[day_of_the_week]}</b> :  {reverse_classes[couple]} "
                         f"<b>для нечетной недели</b> успешно изменено!")
    await state.finish()
    await show_timetable_customization_menu(message)


@dp.message_handler(state=GetCouple.GetNotChangeCouple)
async def ask_audience_number(message: types.Message, state: FSMContext):
    callback_data = await state.get_data()
    message_id = callback_data.get("message_id")
    day_of_the_week = callback_data.get("day_of_the_week")
    couple = callback_data.get("couple")
    await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_id)
    await edit_couple_name_odd(day_of_the_week + str(couple), message.text)
    await edit_couple_name_even(day_of_the_week + str(couple), message.text)
    await message.answer(f"Название <b>постоянной</b> пары <b>{days[day_of_the_week]}</b> :  {reverse_classes[couple]} "
                         f"успешно изменено!")
    await state.finish()
    await show_timetable_customization_menu(message)
