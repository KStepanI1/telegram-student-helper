from .start import dp
from .help import dp
from app.handlers.users.menu.menu import dp
from app.handlers.users.menu.subjects_customization import dp
from app.handlers.users.menu.events_customization import dp
from app.handlers.users.timetable.timetable_customization import dp
from app.handlers.users.menu.teachers_customization import dp
from app.handlers.users.other.commands import dp
from app.handlers.users.other.subscribe import dp
from app.handlers.users.other.admins import dp
from app.handlers.users.other.admin_commands import dp

__all__ = ["dp"]