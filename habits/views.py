from django_celery_beat.models import PeriodicTask, CrontabSchedule
from pytz import timezone
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.utils import json

from habits.models import Habit
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer


class HabitPageNumberPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page size'
    max_page_size = 10


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated & IsOwner]
    pagination_class = HabitPageNumberPagination

    def get_queryset(self):
        """
        Get personal and public habits or only public habits with key 'is_public=true'
        """
        user = self.request.user

        if self.request.query_params:  # http://127.0.0.1:8000/api/habits/?is_public=true
            return Habit.objects.filter(is_public=True).order_by('id')
        else:
            return Habit.objects.filter(Q(user=user) | Q(is_public=True)).order_by('id')

    def perform_create(self, serializer):

        instance = serializer.save()

        crontab, _ = CrontabSchedule.objects.update_or_create(
            minute=instance.task_crontab['minute'] if instance.task_crontab['hour'] else '*',
            hour=instance.task_crontab['hour'] if instance.task_crontab['hour'] else '*',
            day_of_week=instance.task_crontab['day_of_week'] if instance.task_crontab['day_of_week'] else '*',
            day_of_month=instance.task_crontab['day_of_month'] if instance.task_crontab['day_of_month'] else '*',
            month_of_year=instance.task_crontab['month_of_year'] if instance.task_crontab['month_of_year'] else '*',
            timezone=timezone("Europe/Moscow"),
        )

        task = PeriodicTask.objects.create(
            crontab=crontab,
            name=f"habit: {instance.id} {instance.operation}",
            task="habits.tasks.task_send_tg",
            kwargs=json.dumps(
                {
                    "habit_id": instance.id,
                }
            ),
        )

        print('instance.task_crontab', instance.task_crontab)
        print('instance.task', instance.task)
        print('task', task)

        instance.task = task
        instance.user = self.request.user

        instance.save()
