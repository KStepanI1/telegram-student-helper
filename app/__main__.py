from aiogram import Dispatcher
from aiogram.utils import executor

from app import utils
from app.config import WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_URL
from app.handlers.users.menu.events_customization import delete_past_event
from app.handlers.users.timetable.timetable import update_date
from app.loader import dp, scheduler, ssl_context, bot, SSL_CERTIFICATE

# The configuration of the modules using import
from app import handlers, middlewares, filters
from app.utils.db_api import db_gino
from app.utils.db_api.db_gino import db
from app.utils.misc.texts.timetable import set_timetable


async def first_time_bot_runer():
    # -----------------------------------------------------
    # use this function when you run your bot at first time
    # -----------------------------------------------------

    await set_timetable()


def scheduler_jobs():
    scheduler.add_job(delete_past_event, "cron", day_of_week="mon-sun", hour=0, minute=1)
    scheduler.add_job(update_date, "cron", day_of_week="mon-sun", hour=0, minute=0)


async def on_startup(dispatcher: Dispatcher):
    await bot.set_webhook(
        url=WEBHOOK_URL,
        certificate=SSL_CERTIFICATE
    )
    await utils.set_default_commands(dispatcher)
    await db_gino.on_startup(dp)
    await delete_past_event()
    scheduler_jobs()
    await update_date()
    await utils.on_startup_notify(dispatcher)


if __name__ == '__main__':
    utils.setup_logger("INFO", ["sqlalchemy.engine", "aiogram.bot.api"])
    scheduler.start()
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
        ssl_context=ssl_context
    )
