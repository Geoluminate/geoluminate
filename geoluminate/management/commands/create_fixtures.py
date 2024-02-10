from django.core.management.base import BaseCommand
from django.db import transaction

from geoluminate.factories import OrganizationFactory, ProjectFactory, UserFactory


class Command(BaseCommand):

    # allow argruments to be passed to the command
    def add_arguments(self, parser):
        parser.add_argument(
            "--users",
            type=int,
            default=75,
            help="The number of personal contributors to create",
        )
        parser.add_argument(
            "--orgs",
            type=int,
            default=25,
            help="The number of organizational contributors to create",
        )
        parser.add_argument(
            "--projects",
            type=int,
            default=12,
            help="The number of projects to create",
        )

    def handle(self, users=75, orgs=25, projects=12, *args, **options):

        try:
            with transaction.atomic():
                # this will create 100 Contributor objects, 75 Personal and 25 Organizational
                print(f"Creating {users} personal contributors...")
                users = UserFactory.create_batch(users)

                print(f"Creating {orgs} organizational contributors...")
                orgs = OrganizationFactory.create_batch(orgs)

                # create projects. 15 projects (default) creates ~1000 related samples
                print(f"Creating {projects} projects...")
                projects = ProjectFactory.create_batch(projects)
        except Exception as e:
            print(e)
            print("An error occurred. Rolling back changes...")
            raise
