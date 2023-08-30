from django.core.management.base import BaseCommand

from geoluminate.utils import create_fixtures


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_fixtures()
