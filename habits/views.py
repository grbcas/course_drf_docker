from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from habits.models import Habit
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer
from rest_framework.generics import ListAPIView


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

        if self.request.query_params['is_public']:  # http://127.0.0.1:8000/api/habits/?is_public=true
            return Habit.objects.filter(is_public=True).order_by('id')
        else:
            return Habit.objects.filter(Q(user=user) | Q(is_public=True)).order_by('id')
