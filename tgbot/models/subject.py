from asgiref.sync import sync_to_async

from django_project.usersmanage.models import Subject


@sync_to_async
def get_all_subjects():
    return Subject.objects.all()
