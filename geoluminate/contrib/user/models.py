from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from invitations.base_invitation import AbstractBaseInvitation
from taggit.managers import TaggableManager

from geoluminate.contrib.core.choices import iso_639_1_languages
from geoluminate.contrib.core.models import Contribution, Dataset, Project, Sample

from .managers import UserManager


class Identifier(models.Model):
    """A model for storing identifiers for users and organisations."""

    user = models.ForeignKey("user.Contributor", related_name="identifiers", on_delete=models.CASCADE)
    identifier = models.CharField(max_length=255, verbose_name=_("identifier"))
    scheme = models.CharField(max_length=255, verbose_name=_("scheme"))
    url = models.URLField(verbose_name="URL", blank=True, null=True)

    def __str__(self):
        return self.identifier


class User(AbstractUser):
    """A custom user model with email as the primary identifier. The fields align with the W3C Organization and Person
    schema.org types. See https://schema.org/Person"""

    objects = UserManager()  # type: ignore[var-annotated]

    # username = None  # type: ignore[assignment]
    email = models.EmailField(_("email address"), unique=True)

    profile = models.OneToOneField(
        "user.Contributor", related_name="user", on_delete=models.CASCADE, null=True, blank=True
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.get_full_name()

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.profile = Contributor.objects.create(name=self.get_full_name())
        super().save(*args, **kwargs)

    @property
    def username(self):
        return self.get_full_name()

    def get_provider(self, provider: str):
        qs = self.socialaccount_set.filter(provider=provider)  # type: ignore[attr-defined]
        return qs.get() if qs else None

    @property
    def orcid(self):
        return self.get_provider("orcid")

    def get_absolute_url(self):
        return reverse("user:profile", kwargs={"pk": self.pk})

    @property
    def profile_image(self):
        """Return the profile image of the user if it exists, otherwise return the default profile image."""
        if self.profile.image:
            return self.profile.image.url
        return settings.DEFAULT_PROFILE_IMAGE


class Contributor(models.Model):
    """A Contributor is a person or organisation that makes a contribution to a project, dataset, sample or measurement
    within the database. This model stores publicly available information about the contributor that can be used
    for proper attribution and formal publication of datasets. The fields are designed to align with the DataCite
    Contributor schema."""

    image = models.ImageField(
        upload_to="profile_images/",
        verbose_name=_("profile image"),
        help_text=_("A profile image for the contributor."),
        blank=True,
        null=True,
    )

    name = models.CharField(
        max_length=512,
        verbose_name=_("display name"),
        help_text=_("This name is displayed publicly within the website."),
    )

    about = models.TextField(null=True, blank=True)

    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    interests = TaggableManager(
        _("interests"), help_text=_("A list of research interests for the contributor."), blank=True
    )

    lang = models.CharField(
        max_length=255,
        verbose_name=_("language"),
        help_text=_("Language of the contributor."),
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("contributor")
        verbose_name_plural = _("contributors")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("community:profile", kwargs={"pk": self.pk})

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

    def get_datasets(self):
        return Dataset.objects.filter(contributors__profile=self).all()

    def get_samples(self):
        return Contribution.objects.filter(
            profile=self,
            content_type=ContentType.objects.get_for_model(Sample),
        ).all()

    def get_projects(self):
        return Project.objects.filter(contributors__profile=self).all()


class Invitations(AbstractBaseInvitation):
    pass
