from django.urls import path, include
from rest_framework import routers
from habits.apps import HabitsConfig

app_name = HabitsConfig.name

router = routers.SimpleRouter()

router.register(r'habit', HabitViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),   # http://127.0.0.1:8000/api/v1/habit/
]
