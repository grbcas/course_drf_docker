from rest_framework.test import APITestCase
from habits.services.telegram import telegram_bot_message
from users.models import User


class HabitAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            username='test_user',
            password='user@user.user',
            telegram_username='@test_user',
            telegram_uid='559773959',
        )

    def test_telegram_bot_message(self):
        """check telegram request response"""

        response = telegram_bot_message("test message", self.user.telegram_uid)

        # response = {'ok': True,
        #             'result': {'message_id': 140, 'from': {'id': 6542037151, 'is_bot': True, 'first_name': 'skybot_27',
        #                                                    'username': 'skybot27_bot'},
        #             'chat': {'id': 559773959, 'first_name': 'Alexander', 'username': 'grbcas',
        #             'type': 'private'}, 'date': 1701194543,
        #             'text': 'test'}}

        # assert response['ok'] is True

        self.assertEqual(response['ok'], True)
