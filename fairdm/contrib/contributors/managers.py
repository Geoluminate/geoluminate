from django.contrib.auth.models import BaseUserManager
from django.db import models
from polymorphic.managers import PolymorphicManager


class UserManager(BaseUserManager, PolymorphicManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = False

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class ContributionManager(models.QuerySet):
    def by_role(self, role):
        """Returns all contributions with the given role"""
        return self.filter(roles__contains=role)

    # def get_contact_persons(self):
    #     return self.filter(roles__contains=ContributionRoles.CONTACT_PERSON)

    # def lead_contributors(self):
    #     """Returns all project leads"""
    #     return self.filter(roles__contains=ContributionRoles.PROJECT_LEADER)

    # def funding_contributors(self):
    #     """Returns all project leads"""
    #     return self.filter(roles__contains=ContributionRoles.SPONSOR)
