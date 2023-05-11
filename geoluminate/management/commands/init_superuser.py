from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.exists():
            user = settings.ADMINS[0]
            email = user[1]
            password = "admin"  # noqa: S105
            print(
                f"Creating superuser account for {email} with password 'admin'. Be sure to change this as soon as"
                " possible!"
            )
            admin = User.objects.create_superuser(email=email, password=password)
            admin.save()
        else:
            print("This command only works when no users exists.")
