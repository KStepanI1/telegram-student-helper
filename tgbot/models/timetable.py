import logging
from typing import List

from asgiref.sync import sync_to_async

from django_project.usersmanage.models import Timetable
from tgbot.misc.auxiliary_sets import days


@sync_to_async
def get_timetable_for(weekday) -> List[Timetable]:
    return Timetable.objects.filter(weekday__code=weekday).all()
