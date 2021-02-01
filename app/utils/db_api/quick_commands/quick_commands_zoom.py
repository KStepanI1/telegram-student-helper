from asyncpg import UniqueViolationError

from app.utils.db_api.schemas.zoom_links import ZoomLink


async def add_link(**kwargs):
    try:
        link = ZoomLink(**kwargs)
        await link.create()

    except UniqueViolationError:
        pass


async def select_link(subject_name):
    link = await ZoomLink.query.where(ZoomLink.subject_name == subject_name).gino.first()
    return link


async def select_all_links():
    links = await ZoomLink.query.gino.all()
    return links

