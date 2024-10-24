import pytest
from django.test import TestCase

from geoluminate.contrib.contributors.models import Contributor
from geoluminate.factories import (
    OrganizationFactory,
    PersonFactory,
)


@pytest.fixture
@pytest.mark.django_db
def user():
    yield PersonFactory()


@pytest.fixture
@pytest.mark.django_db
def organization():
    return OrganizationFactory()


@pytest.fixture
@pytest.mark.django_db
def unregistered_user():
    return PersonFactory()


@pytest.mark.django_db
class TestPersonFactory:
    def test_factory_create(self, user):
        assert isinstance(user, Contributor)
        assert user.name is not None
        assert user.profile is not None
        assert user.affiliations.count() > 0

    def test_user_relationship(self):
        self.assertIsNotNone(self.obj.user)

    def test_has_no_organization(self):
        self.assertIsNone(self.obj.organization)


class TestOrganizationFactory(TestCase):
    def setUp(self):
        self.obj = OrganizationFactory()

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
