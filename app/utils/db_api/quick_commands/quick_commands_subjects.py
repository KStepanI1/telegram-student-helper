from asyncpg import UniqueViolationError

from app.utils.db_api.schemas.subjects import Subject
from app.utils.db_api.schemas.zoom_links import ZoomLink


async def add_subject(**kwargs):
    try:
        await Subject(**kwargs).create()
    except UniqueViolationError:
        pass


async def select_all_subjects():
    subjects = await Subject.query.gino.all()
    return subjects


async def select_subject(subject_id):
    subject = await Subject.query.where(Subject.subject_id == subject_id).gino.first()
    return subject


async def delete_subject(subject_id):
    subject = await select_subject(subject_id)
    await ZoomLink.delete.where(ZoomLink.subject_name == subject.subject_name).gino.first()
    await Subject.delete.where(Subject.subject_id == subject_id).gino.first()
