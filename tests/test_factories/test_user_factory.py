from django.contrib.auth import get_user_model
from django.test import TestCase

from geoluminate.factories import UserFactory

User = get_user_model()


class TestUserFactory(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_user_creation(self):
        self.assertIsInstance(self.user, User)
        self.assertEqual(self.user.email, f"{self.user.first_name}.{self.user.last_name}@fakeuser.org")

    def test_profile_linked_to_user(self):
        self.assertEqual(self.user.profile.user, self.user)

    def test_user_has_organizations(self):
        self.assertTrue(1 <= len(self.user.organizations_organization.count()) <= 4)

    def test_user_and_profile_same_name(self):
        self.assertEqual(f"{self.user.first_name} {self.user.last_name}", self.user.profile.name)

    def test_password_post_generation(self):
        self.assertTrue(self.user.check_password(self.user.password))
