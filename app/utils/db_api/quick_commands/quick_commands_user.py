from typing import List

from asyncpg import UniqueViolationError

from app.utils.db_api.db_gino import db
from app.utils.db_api.schemas.user import User


async def add_user(**kwargs):
    try:
        user = User(**kwargs)
        await user.create()

    except UniqueViolationError:
        pass


async def update_user(id: int, name: str, subscription: bool, admin: bool, full_name: str=None):
    await User.update.values(name=name).where(
        User.id == id
    ).gino.first()
    await User.update.values(subscription=subscription).where(
        User.id == id
    ).gino.first()
    await User.update.values(admin=admin).where(
        User.id == id
    ).gino.first()
    if full_name:
        await User.update.values(full_name=full_name).where(
            User.id == id
        ).gino.first()


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def select_user(id: int):
    user = await User.query.where(User.id == id).gino.first()
    return user


async def count_users():
    total = await db.func.count(User.id).gino.scalar()
    return total


async def update_user_email(id, email):
    user = await User.get(id)
    await user.update(email=email).apply()


async def update_subscribe_status(user_id, subscribe_status):
    await User.update.values(subscription=subscribe_status).where(
        User.id == user_id
    ).gino.first()


async def update_admin_status(user_id, admin_status):
    await User.update.values(admin=admin_status).where(
        User.id == user_id
    ).gino.first()


async def select_all_admins() -> List[User]:
    admins = await User.query.where(
        (User.admin == True)
    ).gino.all()
    return admins


async def update_user_full_name(user_id, full_name):
    await User.update.values(full_name=full_name).where(
        User.id == user_id
    ).gino.first()
