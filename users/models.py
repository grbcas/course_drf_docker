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
        verbose_name='Unique telegram uid'
    )

    telegram_uid = models.PositiveIntegerField(unique=True,
                                               verbose_name='Unique telegram chat id',
                                               **NULLABLE)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['telegram_username']
