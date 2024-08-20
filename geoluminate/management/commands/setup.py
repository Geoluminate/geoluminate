import logging
import os

from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import OperationalError, ProgrammingError

User = get_user_model()


logger = logging.getLogger(__name__)


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
        # self.stdout.write(self.style.SUCCESS("This is a success message!"))
        # self.stdout.write(self.style.WARNING("This is a warning message!"))
        # self.stdout.write(self.style.ERROR("This is an error message!"))
        # self.stdout.write(self.style.NOTICE("This is a notice message!"))
        # self.stdout.write(self.style.SQL_FIELD("This is an SQL field message!"))
        # self.stdout.write(self.style.HTTP_INFO("This is an HTTP info message!"))
        # self.stdout.write(self.style.MIGRATE_HEADING("This is an HTTP info message!"))

        try:
            has_users = User.objects.exists()
        except (ProgrammingError, OperationalError):
            # logger.info("Initializing a new project...")
            self.stdout.write(self.style.SUCCESS("Initializing a new database..."))
            has_users = False
            call_command("makemigrations", "--no-input")
        else:
            self.stdout.write(self.style.HTTP_INFO("Database already exists. Skipping initialization..."))

        # Apply all migrations
        call_command("migrate", "--no-input")
        # now we can be sure the database is set up

        # 1. Create superuser if no users exist
        if not has_users:
            self.stdout.write(self.style.MIGRATE_HEADING("Creating superuser"))
            call_command("createsuperuser", "--no-input")
            if settings.DEBUG:
                self.stdout.write("Login with:")
                self.stdout.write(self.style.HTTP_INFO("EMAIL: "), ending="")
                self.stdout.write(f"{os.environ.get('DJANGO_SUPERUSER_EMAIL')}")
                self.stdout.write(self.style.HTTP_INFO("PASSWORD: "), ending="")
                self.stdout.write(f"{os.environ.get('DJANGO_SUPERUSER_PASSWORD')}")
                self.stdout.write("You can customize these defaults in your stack.local.env file.")

        # 2. Load creative commons license fixtures
        try:
            self.stdout.write(self.style.MIGRATE_HEADING("Loading default Open Source licenses"))
            call_command("loaddata", "creativecommons")
        except CommandError:
            self.stdout.write(self.style.WARNING("No licenses found. You will need to manually add your own."))

        # # 3. Load initial data
        # if os.environ.get("DJANGO_ENV") == "staging":
        #     try:
        #         call_command("loaddata", "demo")
        #     except CommandError:
        #         print("Failed to load initial data")

        # # 4. Load test data
        # if os.environ.get("DJANGO_ENV") == "staging":
        #     call_command("loaddata", "test_data")

        # 5. Update site domain and name
        self.stdout.write(self.style.HTTP_INFO("Synchronizing site name with settings..."))
        site = Site.objects.get(id=settings.SITE_ID)
        self.stdout.write(f"Site name: {settings.SITE_NAME}, Site Domain: {settings.SITE_DOMAIN}")
        site.domain = settings.SITE_DOMAIN
        site.name = settings.SITE_NAME
        site.save()
