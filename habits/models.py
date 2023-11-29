from django.db import models
from django_celery_beat.models import PeriodicTask

from users.models import User


NULLABLE = {'null': True, 'blank': True}

# import schedule
# schedule.Scheduler
# class Schedule(models.Model):


class Habit(models.Model):

    SCHEDULE = [(1, 'mon'), (2, 'tue'), (3, 'wed'), (4, 'thu'), (5, 'fri'), (6, 'sat'), (7, 'sun')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', **NULLABLE)
    place = models.CharField(max_length=200, verbose_name='Place', **NULLABLE)
    operation = models.CharField(max_length=200, verbose_name='Operation')

    schedule = models.PositiveSmallIntegerField(choices=SCHEDULE, verbose_name='Habit schedule', **NULLABLE)

    task_crontab = models.JSONField()
    task = models.OneToOneField(PeriodicTask, on_delete=models.SET_NULL, **NULLABLE)

    related_habit = models.ForeignKey('Habit', on_delete=models.SET_NULL, verbose_name='related habit', **NULLABLE)
    duration = models.DurationField(verbose_name='Duration')
    reward = models.CharField(max_length=200, verbose_name='Reward', **NULLABLE)
    is_pleasant = models.BooleanField(default=False, verbose_name='Pleasant habit')
    is_public = models.BooleanField(default=False, verbose_name='Public habit')

    def __str__(self):
        return f'{self.operation}'

    class Meta:
        verbose_name = 'Habit'
        verbose_name_plural = 'Habits'
