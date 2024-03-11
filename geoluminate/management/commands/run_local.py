from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run makemigrations, migrate, and runserver commands in sequence. Also creates a superuser if none exist."

    def handle(self, *args, **options):
        call_command("makemigrations")
        call_command("migrate")
        call_command("init_superuser")
        call_command("runserver", "0.0.0.0:8000")
        # call_command("runserver_plus", "0.0.0.0:8000")
