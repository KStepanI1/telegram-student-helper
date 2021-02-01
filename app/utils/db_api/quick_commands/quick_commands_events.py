from typing import List

from asyncpg import UniqueViolationError
from sqlalchemy import and_

from app.utils.db_api.schemas.events import Events
from app.utils.db_api.schemas.subjects import Subject


async def add_event(**kwargs):
    try:
        event = Events(**kwargs)
        await event.create()

    except UniqueViolationError:
        pass


async def select_event(event_id):
    return await Events.query.where(Events.event_id == event_id).gino.first()


async def select_all_events():
    events = await Events.query.gino.all()
    return events


async def delete_event(event_id):
    await Events.delete.where(Events.event_id == event_id).gino.first()


async def get_events(subject_name) -> List[Events]:
    evemts = await Events.query.where(
        and_(Events.subject_name == subject_name)
    ).gino.all()
    return evemts
