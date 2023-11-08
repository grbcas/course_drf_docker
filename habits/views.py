from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer


class HabitPageNumberPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page size'
    max_page_size = 10


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated & IsOwner]
    pagination_class = HabitPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return Habit.objects.filter(user=user)
