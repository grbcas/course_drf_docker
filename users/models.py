from django.db import models
from django.contrib.auth.models import AbstractUser

from users.validators import TelegramNicknameValidator

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    """
    User model
    """

    telegram_username = models.CharField(
        max_length=150,
        unique=True,
        validators=[TelegramNicknameValidator()],
        verbose_name='Unique telegram username',
        **NULLABLE
    )

    telegram_uid = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Unique telegram chat id',
        **NULLABLE
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['telegram_uid']

    def __str__(self):
        return f'{self.pk} {self.username} {self.telegram_uid}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
