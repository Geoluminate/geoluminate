from django.core.management.base import BaseCommand
from django.db import transaction

from geoluminate.factories import (
    OrganizationalContributorFactory,
    PersonalContributorFactory,
    ProjectFactory,
)


class Command(BaseCommand):
    # allow argruments to be passed to the command
    def add_arguments(self, parser):
        parser.add_argument(
            "--users",
            type=int,
            default=50,
            help="The number of personal contributors to create",
        )
        parser.add_argument(
            "--orgs",
            type=int,
            default=15,
            help="The number of organizational contributors to create",
        )
        parser.add_argument(
            "--projects",
            type=int,
            default=6,
            help="The number of projects to create",
        )

    def handle(self, users, orgs, projects, *args, **options):
        try:
            with transaction.atomic():
                # this will create 100 Contributor objects, 75 Personal and 25 Organizational
                print(f"Creating {users} personal contributors...")
                users = PersonalContributorFactory.create_batch(users)

                print(f"Creating {orgs} organizational contributors...")
                orgs = OrganizationalContributorFactory.create_batch(orgs)

                # unclaimed = UnclaimedContributorFactory.create_batch(10)

                # create projects. 15 projects (default) creates ~1000 related samples
                print(f"Creating {projects} projects...")
                projects = ProjectFactory.create_batch(projects)
        except Exception as e:
            print(e)
            print("An error occurred. Rolling back changes...")
            raise
