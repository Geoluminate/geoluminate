import os

from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management import call_command
from django.core.management.base import BaseCommand

User = get_user_model()


def create_superuser():
    print("Creating new super user...")
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


def update_site():
    site = Site.objects.get(id=settings.SITE_ID)
    site.domain = settings.SITE_DOMAIN
    site.name = settings.SITE_NAME
    site.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        if User.objects.exists():
            print("Skipping new project initialization")
            return

        print("Setting up new project...")

        # 0. Run create and run migrations
        call_command("makemigrations")
        call_command("migrate")

        # 1. Create superuser
        create_superuser()

        # 2. Load creative commons license fixtures
        call_command("loaddata", "creativecommons")

        # 3. Load initial data
        call_command("loaddata", "initial_data")

        # 4. Load test data
        if os.environ.get("DJANGO_ENV") == "staging":
            call_command("loaddata", "test_data")

        # 5. Update site domain and name
        update_site()
