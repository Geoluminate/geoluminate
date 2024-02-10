from django.test import TestCase

from geoluminate.contrib.organizations.models import Organization
from geoluminate.factories import OrganizationFactory


class TestOrganizationFactory(TestCase):
    def setUp(self):
        self.obj = OrganizationFactory()

    def test_factory_creation(self):
        self.assertIsInstance(self.obj, Organization)
        self.assertIsNotNone(self.obj.name)

    def test_profile_generation(self):
        self.assertIsNotNone(self.obj.profile)

    def test_organization_profile_same_naem(self):
        self.assertEqual(self.obj.name, self.obj.profile.name)
