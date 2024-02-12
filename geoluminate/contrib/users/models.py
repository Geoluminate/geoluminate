from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from invitations.base_invitation import AbstractBaseInvitation

from geoluminate.contrib.contributors.managers import PersonalManager
from geoluminate.contrib.contributors.models import Contributor

from .managers import UserManager

USER_OPTIONS = {
    "allow_messages": True,
    "contact": True,
}


class User(AbstractUser):
    """A custom user model with email as the primary identifier. The fields align with the W3C Organization and Person
    schema.org types. See https://schema.org/Person"""

    objects = UserManager()  # type: ignore[var-annotated]

    # username = None  # type: ignore[assignment]
    email = models.EmailField(_("email address"), unique=True)

    # settings = models.JSONField(default=dict, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.get_full_name()

    @property
    def image(self):
        return self.profile.image

    @property
    def username(self):
        if self.profile:
            return str(self.profile)
        return self.get_full_name()

    def get_provider(self, provider: str):
        qs = self.socialaccount_set.filter(provider=provider)  # type: ignore[attr-defined]
        return qs.get() if qs else None

    @property
    def orcid(self):
        return self.get_provider("orcid")

    def get_absolute_url(self):
        return reverse("contributor:detail", kwargs={"uuid": self.profile.uuid})

    @property
    def profile_image(self):
        """Return the profile image of the user if it exists, otherwise return the default profile image."""
        if self.image:
            return self.image.url
        return settings.DEFAULT_PROFILE_IMAGE


class Invitations(AbstractBaseInvitation):
    pass
