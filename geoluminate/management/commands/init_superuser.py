from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        print("Checking for existing users...")
        if not User.objects.exists():
            user = settings.ADMINS[0]
            email = user[1]
            password = "admin"  # noqa: S105
            print(
                f"No users found. Creating superuser account for {email} with password 'admin'. Be sure to change this"
                " as soon as possible!"
            )
            superuser = User.objects.create_superuser(
                email=email,
                password=password,
                first_name="Super",
                last_name="User",
            )
            superuser.save()

            # create user profile

            # verify the users email address without send a confirmation email
            email = EmailAddress.objects.create(user=superuser, email=email, verified=True, primary=True)
            email.save()

        else:
            print("This command only works when no users exists.")
