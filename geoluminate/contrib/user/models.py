from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from invitations.base_invitation import AbstractBaseInvitation

from .managers import UserManager

# from allauth.account.forms import SignupForm


class Identifier(models.Model):
    """A model for storing identifiers for users and organisations."""

    user = models.ForeignKey("user.Profile", related_name="identifiers", on_delete=models.CASCADE)
    identifier = models.CharField(max_length=255, verbose_name=_("identifier"))
    scheme = models.CharField(max_length=255, verbose_name=_("scheme"))
    url = models.URLField(verbose_name=_("url"), blank=True, null=True)

    def __str__(self):
        return self.identifier


class User(AbstractUser):
    """A custom user model with email as the primary identifier."""

    objects = UserManager()  # type: ignore[var-annotated]

    class AcademicTitle(models.TextChoices):
        DR = "Dr.", _("Dr.")
        PROF = "Prof.", _("Prof.")
        # PROF_DR = "Prof. Dr.", _("Prof. Dr.")

    username = None  # type: ignore[assignment]
    email = models.EmailField(_("email address"), unique=True)
    academic_title = models.CharField(
        max_length=5, choices=AcademicTitle.choices, verbose_name=_("academic title"), blank=True, null=True
    )
    profile = models.OneToOneField("user.Profile", related_name="user", on_delete=models.CASCADE, null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}.{self.last_name}"
        return ""

    @property
    def display_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}. {self.last_name}"

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
    """A user profile model that extends the default Django user model. This model is set up
    to closely resemble the DataCite schema for contributors so that user and/or organization data can easily be added
    to datasets ready for publication."""

    name = models.CharField(
        max_length=512,
        verbose_name=_("name"),
        help_text=_(
            "Your preferred name for use in thingsName of the contributor. Will be automatically populated from given"
            " name and family name if left blank."
        ),
        blank=True,
    )

    about = models.TextField(null=True, blank=True)

    lang = models.CharField(
        max_length=255,
        verbose_name=_("language"),
        help_text=_("Language of the contributor."),
        blank=True,
        null=True,
    )

    @property
    def type(self):
        if self.user:
            return "Person"
        else:
            return "Organization"

    @property
    def given(self):
        if self.user:
            return self.user.first_name
        return ""

    @property
    def family(self):
        if self.user:
            return self.user.last_name
        return ""


class Invitations(AbstractBaseInvitation):
    pass
