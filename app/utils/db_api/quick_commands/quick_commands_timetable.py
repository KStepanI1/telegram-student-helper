from asyncpg import UniqueViolationError
from sqlalchemy import and_

from app.utils.db_api.schemas.timetable import Couples


async def add_couple(**kwargs):
    try:
        couple = Couples(**kwargs)
        await couple.create()
    except UniqueViolationError:
        pass


async def edit_couple_name_odd(couple_ui, new_couple_name_odd):
    await Couples.update.values(name_couple_odd=new_couple_name_odd).where(
        Couples.couple_ui == couple_ui
    ).gino.first()


async def edit_couple_name_even(couple_ui, new_couple_name_even):
    await Couples.update.values(name_couple_even=new_couple_name_even).where(
        Couples.couple_ui == couple_ui
    ).gino.first()


async def delete_couple_name_even(couple_ui):
    await Couples.update.values(name_couple_even=None).where(
        Couples.couple_ui == couple_ui
    ).gino.first()


async def delete_couple_name_odd(couple_ui):
    await Couples.update.values(name_couple_odd=None).where(
        Couples.couple_ui == couple_ui
    ).gino.first()


async def select_couple(couple_ui):
    couple = await Couples.query.where(Couples.couple_ui == couple_ui).gino.first()
    return couple


async def select_all_couples_for_day(day_of_week):
    couples = []
    for i in range(6):
        couple = await select_couple(day_of_week + str(i+1))
        couples.append(couple)
    return couples
