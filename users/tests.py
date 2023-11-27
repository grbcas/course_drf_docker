import sys
from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from dotenv import load_dotenv
from rest_framework import status, response
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from django.test.client import Client
import os


class UserTestCase(APITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('users:user_registration')

    def test_user_registration_username(self):

        data_wrong_username = {
            'username': 'user1',
            'password': 'user_pswd',
            'telegram_username': 'wrong_username',
            "telegram_uid": "1"
        }

        response = self.client.post(self.url, data=data_wrong_username)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'telegram_username': ["Invalid telegram nickname"]})

    def test_user_registration(self):

        valid_data = {
            'username': 'user2',
            "password": "user_pswd",
            'telegram_username': '@user2',
            "telegram_uid": "2"
        }

        response = self.client.post(self.url, data=valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {
            'username': 'user2',
            'telegram_username': '@user2',
            'telegram_uid': '2'
            }
        )


class CreateAdminCommandTestCase(TestCase):

    def test_createadmin(self):

        # load_dotenv()
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        password = os.environ.get('ADMIN_PASSWORD', 'admin@admin.admin')
        call_command('createadmin')
        c = Client()
        is_logined = c.login(username=username, password=password)
        self.assertEqual(is_logined, True)
