
from celery.schedules import crontab

app.conf.beat_schedule = {

    'test_beat_schedule': {
        'task': 'tasks.task_message',
        'schedule': crontab(minute='*/1'),
        'args': ('Testing Telegram bot', 5194882396),
    },

    'test_test_print': {
        'task': 'tasks.test_print',
        'schedule': crontab(minute='*/1'),
        'args': ('tasks.test_print',),
    },

}
app.conf.timezone = "Europe/Moscow"

