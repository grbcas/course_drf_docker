# from django.test import TestCase
#
# # Create your tests here.
# class HabitApiTest(TestCase):
#     url =

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from django.core import serializers

from habits.models import Habit
from users.models import User


class HabitAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            username='test_user',
            password='user@user.user',
            telegram_username='@test_user',
            telegram_uid='5194882396',
        )



        data = [
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 1,
                        "name": "test_lesson",
                        "description": None,
                        "course": 1,
                        "link_video": None
                    }
                ]
            }
        ]

        # self.habit = Habit.objects.create(
        #         place="place",
        #         operation="operation_2",
        #         schedule=3,
        #         duration="00:00:03",
        #         reward=None,
        #         is_pleasant=True,
        #         is_public=None,
        #         related_habit=None,
        #         task_crontab=
        #             {
        #                 "minute": "*/1",
        #                 "hour": "*"
        #             }
        # )

        self.client.force_authenticate(user=self.user)

    def test_get_habits(self):
        response = self.client.get(reverse('habits:habits_api'))  # ссылка для

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK
                         )

        self.assertEqual(response.json(),
                         {
                             "count": 1,
                             "next": None,
                             "previous": None,
                             "results": [
                                 {
                                     "id": 1,
                                     "name": "test_lesson",
                                     "description": None,
                                     "course": 1,
                                     "link_video": None
                                 }
                             ]
                         }
                         )
