from typing import List

from asgiref.sync import sync_to_async

from bot import logger
from django_project.usersmanage.models import Teacher


@sync_to_async
def get_all_teachers_by(subject_name) -> List[Teacher]:
    try:
        return Teacher.objects.filter(subject__name=subject_name).all()
    except Exception as exception:
        logger.exception(exception)
