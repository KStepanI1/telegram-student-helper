from typing import List

from asgiref.sync import sync_to_async

from bot import logger
from django_project.usersmanage.models import ZoomLink


@sync_to_async
def get_all_links_by(subject_name) -> List[ZoomLink]:
    try:
        return ZoomLink.objects.filter(subject__name=subject_name).all()
    except Exception as exception:
        logger.exception(exception)

