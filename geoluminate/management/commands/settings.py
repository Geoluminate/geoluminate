import pprint

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--app",
            type=str,
            help="Limit output to single app",
        )

    def handle(self, app, *args, **options):
        settings_dict = settings.__dict__
        groups = {}

        for key in settings_dict:
            group = key.split("_")[0]
            if group not in groups:
                groups[group] = {}
            groups[group][key] = settings_dict[key]

        if app:
            if app in groups:
                print(f"\n{app.upper()}")
                print("=" * 80)
                pprint.pprint(groups[app])
            else:
                print(f"No settings found for {app}")
        else:
            for group in groups:
                print(f"\n{group.upper()}")
                print("=" * 80)
                pprint.pprint(groups[group])
