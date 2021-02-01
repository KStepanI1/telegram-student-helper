from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, ParseMode

from app import config
from app.filters.IsAdmin import IsAdminFilter
from app.keyboards.inline.cancel_keyboard import set_cancel_keyboard
from app.loader import dp, bot
from app.states.admin_states import GetAdmin, DeleteAdmin
from app.utils.db_api.quick_commands.quick_commands_user import update_admin_status, select_user, select_all_admins, \
    update_user_full_name
from app.utils.misc.texts.admins_text import admins_text, admins_for_user_text


async def new_admin_added_mailing(editor, user):
    text = [f"<b>Пользователь</b>: {user.name}",
            f"<b>Имя</b>: {user.full_name}",
            f"<b>id</b>: {user.id}",
            f"Был <b>наделен правами администратора</b> юзером:",
            f"<b>Пользователь</b>: {editor.name}",
            f"<b>Имя</b>: {editor.full_name}",
            f"<b>id</b>: {editor.id}"]

    await bot.send_message(chat_id=config.SUPERUSER_ID[0],
                           text="\n".join(text))


@dp.message_handler(Command("get_id"))
async def send_user_id(message: types.Message):
    await message.answer(f"Твой id: {message.from_user.id}")


@dp.message_handler(Command("add_admin"), user_id=config.SUPERUSER_ID[0])
async def ask_user_id(message: types.Message, state: FSMContext):
    message = await message.answer("Введи id юзера", reply_markup=set_cancel_keyboard)
    await state.update_data(message_id=message.message_id)
    await GetAdmin.GetId.set()


@dp.message_handler(state=GetAdmin.GetId)
async def check_fullname_new_admin(message: types.Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get("message_id")
    await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_id)
    if message.text.isdigit():
        user_id = int(message.text)
        user = await select_user(user_id)
        if not user.full_name:
            await state.update_data(user_id=user_id)
            await message.answer(
                "Введите имя и фамилию нового администратора (сначала <b>имя</b>, потом <b>фамилию</b>)",
                reply_markup=set_cancel_keyboard)
            await GetAdmin.GetFullname.set()
        else:
            await add_new_admin(message, state, user_id)
    else:
        await state.finish()
        await message.answer("id введен некоректно!")


@dp.message_handler(state=GetAdmin.GetFullname)
async def save_user_full_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    await update_user_full_name(user_id, message.text)
    await add_new_admin(message, state, user_id)


async def add_new_admin(message, state, user_id):
    await update_admin_status(user_id, True)
    user = await select_user(user_id)
    editor = await select_user(message.from_user.id)
    if int(message.from_user.id) != int(config.SUPERUSER_ID[0]):
        await message.answer(f"Пользователь: {user.name}\n"
                             f"Имя: {user.full_name}\n"
                             f"id: {user.id}\n"
                             f"Успешно наделен правами администратора")
    await new_admin_added_mailing(editor, user)
    await state.finish()


@dp.message_handler(Command("get_admins"), IsAdminFilter())
async def show_admins_list(message: types.Message):
    admins = await select_all_admins()
    admins_list = ["<b>Список администраторов</b>"]
    admin_number = 1
    for admin in admins:
        admins_list.append(admins_text.format(
            number=admin_number,
            user_name=admin.name,
            full_name=admin.full_name,
            admin_id=admin.id
        ))
        admin_number += 1
    await message.answer("\n".join(admins_list))


@dp.message_handler(Command("show_admins"))
async def show_admins_list(message: types.Message):
    admins = await select_all_admins()
    admins_list = ["<b>Список администраторов</b>"]
    admin_number = 1
    for admin in admins:
        admins_list.append(admins_for_user_text.format(
            number=admin_number,
            full_name=admin.full_name
        ))
        admin_number += 1
    await message.answer("\n".join(admins_list))


@dp.message_handler(Command("remove_admin"), user_id=config.SUPERUSER_ID[0])
async def ask_userid_for_remove_from_admins(message: types.Message, state: FSMContext):
    message = await message.answer("Введи id юзера", reply_markup=set_cancel_keyboard)
    await state.update_data(message_id=message.message_id)
    await DeleteAdmin.GetId.set()


@dp.message_handler(state=DeleteAdmin.GetId)
async def remove_user_from_admin(message: types.Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get("message_id")
    await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_id)
    if message.text.isdigit():
        user_id = int(message.text)
        user = await select_user(user_id)
        if user.admin:
            await update_admin_status(user.id, False)
            await message.answer(f"<b>Пользователь</b>: {user.name}\n"
                                 f"<b>Имя</b>: {user.full_name}\n"
                                 f"<b>id</b>: {user.id}\n"
                                 f"Удален из администраторов!")
            await state.finish()
        else:
            await message.answer("Пользователь не является администратором")
    else:
        await message.answer("id введен некоректно!")


@dp.callback_query_handler(text_contains="cancel", state="*")
async def cancel_add_admin(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await state.finish()
    await call.message.answer("Действие отменено!")
