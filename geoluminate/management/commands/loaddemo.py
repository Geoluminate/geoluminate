"""A management command to load a demo dataset into the database."""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, fixture="demo", *args, **options):
        """Load the demo dataset into the database."""
        from django.core.management import call_command

        call_command("loaddata", fixture, *args, **options)
