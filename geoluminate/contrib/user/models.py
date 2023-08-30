from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from invitations.base_invitation import AbstractBaseInvitation
from taggit.managers import TaggableManager

from geoluminate.contrib.project.choices import iso_639_1_languages
from geoluminate.contrib.project.models import Contributor, Dataset, Project, Sample

from .managers import UserManager


class Identifier(models.Model):
    """A model for storing identifiers for users and organisations."""

    user = models.ForeignKey("user.Profile", related_name="identifiers", on_delete=models.CASCADE)
    identifier = models.CharField(max_length=255, verbose_name=_("identifier"))
    scheme = models.CharField(max_length=255, verbose_name=_("scheme"))
    url = models.URLField(verbose_name="URL", blank=True, null=True)

    def __str__(self):
        return self.identifier


class User(AbstractUser):
    """A custom user model with email as the primary identifier."""

    objects = UserManager()  # type: ignore[var-annotated]

    class AcademicTitle(models.TextChoices):
        DR = "Dr.", _("Dr.")
        PROF = "Prof.", _("Prof.")

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

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.profile = Profile.objects.create(name=self.full_name())
        super().save(*args, **kwargs)

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
        blank=True,
    )

    # publishing_name = models.CharField(
    #     max_length=512,
    #     verbose_name=_("publishing name"),
    #     help_text=_(
    #         "This name is displayed publicly within the website and may be transmitted to data publishing services."
    #         " If you typically publish under a pseudonym (e.g maiden name), you can specifiy that here. It is also displayed on your public profile on this site."
    #     ),
    #     blank=True,
    # )

    about = models.TextField(null=True, blank=True)

    # slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    # interests = TaggableManager(
    #     _("interests"), help_text=_("A list of research interests for the contributor."), blank=True
    # )

    # languages = models.CharField(
    #     max_length=2,
    #     choices=iso_639_1_languages,
    #     verbose_name=_("alternate language"),
    #     help_text=_("Alternate language of the contributor."),
    #     blank=True,
    #     null=True,
    # )

    CONTRIBUTOR_STATUS = (
        ("active", _("Active")),
        ("inactive", _("Inactive")),
        # ("suspended", _("Suspended")),
        ("unclaimed", _("Unclaimed")),
        ("deleted", _("Deleted")),
    )

    # status = models.CharField(
    #     max_length=12,
    #     choices=CONTRIBUTOR_STATUS,
    #     verbose_name=_("status"),
    #     help_text=_("Status of the contributor."),
    #     default="inactive",
    # )
    lang = models.CharField(
        max_length=255,
        verbose_name=_("language"),
        help_text=_("Language of the contributor."),
        blank=True,
        null=True,
    )

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

        # return Contributor.objects.filter(
        #     profile=self,
        #     content_type__model=ContentType.objects.get_for_model(Dataset),
        # ).all()

    def get_samples(self):
        return Contributor.objects.filter(
            profile=self,
            content_type=ContentType.objects.get_for_model(Sample),
        ).all()

    def get_projects(self):
        return Project.objects.filter(contributors__profile=self).all()
        # return Contributor.objects.filter(
        #     profile=self,
        #     content_type=ContentType.objects.get_for_model(Project),
        # ).all()


class Invitations(AbstractBaseInvitation):
    pass
