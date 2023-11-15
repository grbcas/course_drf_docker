from django.urls import path, include
from rest_framework import routers
from habits.apps import HabitsConfig
from habits.views import HabitViewSet

app_name = HabitsConfig.name

router = routers.SimpleRouter()

router.register(r'habits', viewset=HabitViewSet, basename='habits')

urlpatterns = [
    path('api/', include(router.urls)),

    # path('public_habits/', HabitAPIView.as_view(), name='public_habits')
]
