from rest_framework import viewsets

from habits.models import Habit


class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
