from django.core.management.base import BaseCommand

from geoluminate.factories import OrganizationFactory, ProjectFactory, UserFactory


class Command(BaseCommand):
    def handle(self, users=75, orgs=25, projects=12, *args, **options):
        # this will create 100 Contributor objects, 75 Personal and 25 Organizational
        users = UserFactory.create_batch(users)
        orgs = OrganizationFactory.create_batch(orgs)

        # create projects. 15 projects (default) creates ~1000 related samples
        projects = ProjectFactory.create_batch(projects)
