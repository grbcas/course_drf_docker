from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            username='test_user',
            password='user@user.user',
            telegram_username='@test_user',
            telegram_uid='12345',
        )

        self.habit = Habit.objects.create(
            place="place",
            operation="operation",
            schedule=3,
            duration="00:00:03",
            reward=None,
            is_pleasant=True,
            is_public=True,
            related_habit=None,
            task_crontab={
                'day_of_month': '*',
                'day_of_week': '*',
                'hour': '*',
                'minute': '*/1',
                'month_of_year': '*'
            },
            user=self.user
        )

        self.client.force_authenticate(user=self.user)

    def test_habit_retrieve(self):
        response = self.client.get(reverse('habits:habits_api-detail', str(self.habit.id)))
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(),
                         {
                             "id": self.habit.id,
                             "place": "place",
                             "operation": "operation",
                             "schedule": 3,
                             "task_crontab": {
                                 "hour": "*",
                                 "minute": "*/1",
                                 "day_of_week": "*",
                                 "day_of_month": "*",
                                 "month_of_year": "*"
                             },
                             "duration": "00:00:03",
                             "reward": None,
                             "is_pleasant": True,
                             "is_public": True,
                             "user": self.user.pk,
                             "related_habit": None,
                             'task': None,
        }
        )

    def test_habit_create(self):
        data = {
            "place": "test",
            "operation": "test",
            "schedule": 3,
            "task_crontab": {
                "hour": "*",
                "minute": "*/1",
                "day_of_week": "*",
                "day_of_month": "*",
                "month_of_year": "*"
            },
            "duration": "00:00:03",
            "reward": None,
            "is_pleasant": True,
            "is_public": True,
            "related_habit": None,
            'task': None,
        }

        response = self.client.post(reverse('habits:habits_api-list'), data=data, format="json")
        # print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.json(),
                         {
                             "id": self.habit.id + 1,
                             "place": "test",
                             "operation": "test",
                             "schedule": 3,
                             "task_crontab": {
                                 "hour": "*",
                                 "minute": "*/1",
                                 "day_of_week": "*",
                                 "day_of_month": "*",
                                 "month_of_year": "*"
                             },
                             "duration": "00:00:03",
                             "reward": None,
                             "is_pleasant": True,
                             "is_public": True,
                             "user": self.user.pk,
                             "related_habit": None,
                             'task': 1,
        }
        )

    def test_habit_update(self):
        data = {
            "place": "test patch",
        }

        response = self.client.patch(reverse('habits:habits_api-detail', str(self.habit.id)), data=data, format='json')
        # print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(),
                         {
                             "id": self.habit.id,
                             "place": "test patch",
                             "operation": "operation",
                             "schedule": 3,
                             "task_crontab": {
                                 "hour": "*",
                                 "minute": "*/1",
                                 "day_of_week": "*",
                                 "day_of_month": "*",
                                 "month_of_year": "*"
                             },
                             "duration": "00:00:03",
                             "reward": None,
                             "is_pleasant": True,
                             "is_public": True,
                             "user": self.user.pk,
                             "related_habit": None,
                             'task': None,
        }
        )

    def test_habit_delete(self):
        response = self.client.delete(reverse('habits:habits_api-detail', str(self.habit.id)))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_habits(self):
        response = self.client.get(reverse('habits:habits_api-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.json())
        self.assertEqual(response.json(),
                         {
                             "count": 1,
                             "next": None,
                             "previous": None,
                             "results": [
                                 {
                                     "id": self.habit.id,
                                     "place": "place",
                                     "operation": "operation",
                                     "schedule": 3,
                                     "task_crontab": {
                                         'day_of_month': '*',
                                         'day_of_week': '*',
                                         'hour': '*',
                                         'minute': '*/1',
                                         'month_of_year': '*'
                                     },
                                     "duration": "00:00:03",
                                     "reward": None,
                                     "is_pleasant": True,
                                     "is_public": True,
                                     "user": self.user.pk,
                                     "task": None,
                                     "related_habit": None
                                 }
                             ]
        }
        )

    def test_habit_validators(self):
        data = {
            "place": "test",
            "operation": "test",
            "schedule": 3,
            "task_crontab": {
                "hour": "*",
                "minute": "*",
                "day_of_week": "*",
                "day_of_month": "1",
                "month_of_year": "*"
            },
            "duration": "10:00:03",
            "reward": "None",
            "is_pleasant": True,
            "is_public": True,
            "related_habit": None,
            'task': None,
        }

        response = self.client.post(reverse('habits:habits_api-list'), data=data, format="json")
        # print(response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(response.json(),
                         {
                             "non_field_errors": [
                                 "The execution time should be no more than 120 seconds.",
                                 "A pleasant habit can't have a reward or a related habit",
                                 "The frequency of the habit should be less than a week"
                             ]
        }
        )
