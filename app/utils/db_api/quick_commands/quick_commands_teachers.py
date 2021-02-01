from typing import List

from asyncpg import UniqueViolationError

from app.utils.db_api.schemas.teachers import Teachers


async def add_teacher(**kwargs):
    try:
        teacher = Teachers(**kwargs)
        await teacher.create()
    except UniqueViolationError:
        pass


async def select_teacher(teacher_id):
    teacher = await Teachers.query.where(Teachers.teacher_id == teacher_id).gino.first()
    return teacher


async def delete_teacher(teacher_id):
    await Teachers.delete.where(Teachers.teacher_id == teacher_id).gino.first()


async def select_all_teachers():
    teachers = await Teachers.query.gino.all()
    return teachers


async def update_teacher_name(teacher_id, new_teacher_name):
    await Teachers.update.values(teacher_name=new_teacher_name).where(
        Teachers.teacher_id == teacher_id
    ).gino.first()


async def update_teacher_mail(teacher_id, new_teacher_mail):
    await Teachers.update.values(teacher_mail=new_teacher_mail).where(
        Teachers.teacher_id == teacher_id
    ).gino.first()


async def get_teachers(subject_name) -> List[Teachers]:
    teachers = await Teachers.query.where(
        (Teachers.subject_name == subject_name)
    ).gino.all()
    return teachers
