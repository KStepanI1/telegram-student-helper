from asgiref.sync import sync_to_async

from django_project.usersmanage.models import User


@sync_to_async
def select_user(user_id: int):
    user = User.objects.filter(user_id=user_id).first()
    return user


@sync_to_async
def add_user(user_id, full_name, username):
    try:
        return User(user_id=int(user_id), name=full_name, username=username).save()
    except Exception:
        return select_user(int(user_id))


@sync_to_async
def select_all_users():
    users = User.objects.all()
    return users


@sync_to_async
def count_users():
    return User.objects.all().count()


@sync_to_async
def update_user(user_id, full_name, username):
    User.objects.filter(user_id=user_id).update(username=username, name=full_name)

