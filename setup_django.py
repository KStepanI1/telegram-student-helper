import os

import django


def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "django_project.student_helper.settings"
    )
    os.environ.update(
        {"DJANGO_ALLOW_ASYNC_UNSAFE": " true"}
    )
    django.setup()


setup_django()