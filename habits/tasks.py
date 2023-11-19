
import logging
from django_celery_beat.models import PeriodicTask
from celery.schedules import crontab

from config.celery import app
from .models import Habit
from .services.telegram import telegram_bot_message

# PeriodicTask.objects.update(last_run_at=None)


@app.task
def task_message(message, chat_id):
    logging.info(">>>>>>>>>task_message uid 559773959")
    telegram_bot_message(message=message, chat_id=chat_id)
    telegram_bot_message("task_message Telegram bot 559773959", 559773959)


@app.task
def check():
    print('I am checking your stuff')


app.conf.beat_schedule = {
    'test_beat_schedule': {
        'task': 'habits.tasks.task_message',
        'schedule': crontab(minute='*/1'),
        'args': ('test_beat_schedule bot 559773959', 559773959),
    },

    'test_beat_2': {
        'task': 'habits.tasks.check',
        'schedule': crontab(),
    },
}
app.conf.timezone = "Europe/Moscow"
