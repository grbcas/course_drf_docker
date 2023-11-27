from dotenv import load_dotenv
from django.core.management import BaseCommand

from config.settings import BASE_DIR
from users.models import User
import os


class Command(BaseCommand):
    """create admin user from credentials from the .env file"""

    def handle(self, *args, **options):

        load_dotenv()

        print('credentials: ', os.getenv('ADMIN_USERNAME', default='admin'),
              os.getenv('ADMIN_PASSWORD', default='admin@admin.admin'))

        user, created = User.objects.get_or_create(
            username=os.getenv('ADMIN_USERNAME', 'admin'),
            is_staff=True,
            is_superuser=True
        )
        if created:
            user.set_password(os.getenv('ADMIN_PASSWORD', 'admin@admin.admin'))
            user.save()
            return f'admin was created'
