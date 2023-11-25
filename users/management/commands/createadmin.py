from dotenv import load_dotenv
from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """create admin user from credentials from the .env file"""

    def handle(self, *args, **options):
        load_dotenv()
        user, created = User.objects.get_or_create(
            # username=load_dotenv('ADMIN_USERNAME'),
            username='admin',
            is_staff=True,
            is_superuser=True
        )
        if created:
            # user.set_password(load_dotenv('ADMIN_PASSWORD'))
            user.set_password('admin@admin.admin')
            user.save()
            return
