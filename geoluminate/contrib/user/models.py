from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from invitations.base_invitation import AbstractBaseInvitation

from .managers import UserManager


class User(AbstractUser):
    objects = UserManager()

    username = None  # type: ignore[assignment]
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}.{self.last_name}"

    # @property
    # def display_name(self):
    #     if self.first_name and self.last_name:
    #         return f"{self.first_name[0]}.{self.last_name}"

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def initials(self) -> str:
        return f"{self.first_name[0]}{self.last_name[0]}"

    def first_l(self) -> str:
        return f"{self.first_name}{self.last_name[0].capitalize()}"

    def get_provider(self, provider: str):
        qs = self.socialaccount_set.filter(provider=provider)  # type: ignore[attr-defined]
        return qs.get() if qs else None

    @property
    def orcid(self):
        return self.get_provider("orcid")

    def get_absolute_url(self):
        return reverse("user:profile", kwargs={"pk": self.pk})

    @cached_property
    def is_db_admin(self):
        return self.groups.filter(name="Database Admin").exists()


class Profile(models.Model):
    is_organization = models.BooleanField(_("is organization?"), default=False)
    name = models.CharField(max_length=255)
    about = models.TextField(null=True, blank=True)


class Invitations(AbstractBaseInvitation):
    pass
