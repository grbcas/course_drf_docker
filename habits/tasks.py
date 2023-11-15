from config.celery import app
from .models import Habit
from .services.telegram import telegram_bot_message

from celery.schedules import crontab


@app.task
def task_message(message, chat_id):
    telegram_bot_message(message=message, chat_id=chat_id)


@app.task
def test_print(arg):
    print(arg)


@app.task
def check():
    print('I am checking your stuff')


app.conf.beat_schedule = {

    'test_beat_schedule': {
        'task': 'tasks.task_message',
        'schedule': crontab(minute='*/1'),
        'args': ('Testing Telegram bot', 559773959),
    },

    'test_test_print': {
        'task': 'tasks.test_print',
        'schedule': crontab(minute='*/1'),
        'args': ('tasks.test_print',),
    },

}
app.conf.timezone = "Europe/Moscow"

# app.conf.beat_schedule = {
#     'run-me-every-ten-seconds': {
#         'task': 'tasks.check',
#         'schedule': 10.0
#     }
# }