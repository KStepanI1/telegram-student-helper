import logging
from typing import List

from asgiref.sync import sync_to_async

from bot import logger
from django_project.usersmanage.models import Timetable


@sync_to_async
def get_timetable_for(weekday) -> List[Timetable]:
    try:
        return Timetable.objects.filter(weekday=weekday).all()
    except Exception as exception:
        logger.exception(exception)
