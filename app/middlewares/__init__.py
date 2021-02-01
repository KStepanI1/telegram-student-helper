from app.loader import dp
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from app.middlewares.throttling import ThrottlingMiddleware

if __name__ == 'app.middlewares':
    dp.middleware.setup(LoggingMiddleware())
    dp.middleware.setup(ThrottlingMiddleware())
