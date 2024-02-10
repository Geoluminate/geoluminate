from django.test import TestCase

from geoluminate.contrib.contributors.models import Contributor
from geoluminate.factories import (
    ContributionFactory,
    OrganizationalContributorFactory,
    PersonalContributorFactory,
    UnclaimedContributorFactory,
)


class TestUnclaimedContributorFactory(TestCase):
    def setUp(self):
        self.obj = UnclaimedContributorFactory()

    def test_factory_creation(self):
        self.assertIsInstance(self.obj, Contributor)
        self.assertIsNotNone(self.obj.name)
        self.assertIsNotNone(self.obj.about)

    def test_has_no_relationships(self):
        self.assertIsNotNone(self.obj.user)
        self.assertIsNotNone(self.obj.organization)


class TestPersonalContributorFactory(TestCase):
    def setUp(self):
        self.obj = PersonalContributorFactory()

    def test_factory_creation(self):
        self.assertIsInstance(self.obj, Contributor)
        self.assertIsNotNone(self.obj.name)
        self.assertIsNotNone(self.obj.about)

    def test_user_relationship(self):
        self.assertIsNotNone(self.obj.user)

    def test_has_no_organization(self):
        self.assertIsNone(self.obj.organization)

    def test_user_profile_same_name(self):
        self.assertEqual(f"{self.obj.user.first_name} {self.obj.user.last_name}", self.obj.name)


class TestOrganizationalContributorFactory(TestCase):
    def setUp(self):
        self.obj = OrganizationalContributorFactory()

    def test_factory_creation(self):
        self.assertIsInstance(self.obj, Contributor)
        self.assertIsNotNone(self.obj.name)
        self.assertIsNotNone(self.obj.about)

    def test_organisation_relationship(self):
        self.assertIsNotNone(self.obj.organization)

    def test_has_no_user(self):
        self.assertIsNone(self.obj.user)

    def test_organization_profile_same_name(self):
        self.assertEqual(self.obj.organization.name, self.obj.name)
