# your_app/management/commands/profile.py
import cProfile
import io
import pstats

from django.core.management.base import BaseCommand
from django.utils import autoreload


class Command(BaseCommand):
    help = "Profiles the Django application."

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting profiler...")
        autoreload.run_with_reloader(self.profile)

    def profile(self):
        pr = cProfile.Profile()
        pr.enable()

        from django.core.management import call_command

        call_command("runserver")

        pr.disable()
        s = io.StringIO()
        sortby = pstats.SortKey.CUMULATIVE
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        with open("profile.txt", "w+") as f:
            f.write(s.getvalue())
