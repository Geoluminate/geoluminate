import random

from django.templatetags.static import static
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import SmartResize
from jsonfield_toolkit.models import ArrayField

# from django.db.models.fields.files import FieldFile
from geoluminate.core.models import AbstractIdentifier, PolymorphicMixin
from geoluminate.core.utils import inherited_choices_factory
from geoluminate.db import models

from . import choices


def profile_image_path(instance, filename):
    """Return the path to the profile image for a contributor."""
    return f"contributors/{instance.pk}.webp"


class Contributor(models.Model, PolymorphicMixin):
    """A Contributor is a person or organisation that makes a contribution to a project, dataset, sample or measurement
    within the database. This model stores publicly available information about the contributor that can be used
    for proper attribution and formal publication of datasets. The fields are designed to align with the DataCite
    Contributor schema."""

    image = ProcessedImageField(
        verbose_name=_("profile image"),
        processors=[SmartResize(600, 600)],
        format="WEBP",
        options={"quality": 60},
        blank=True,
        null=True,
        upload_to=profile_image_path,
    )

    name = models.CharField(
        max_length=512,
        verbose_name=_("preferred name"),
        # help_text=_("This name is displayed publicly within the website."),
    )

    alternative_names = models.JSONField(
        verbose_name=_("alternative names"),
        help_text=_("Any other names by which the contributor is known."),
        null=True,
        blank=True,
        default=list,
    )

    profile = models.TextField(_("profile"), null=True, blank=True)

    # interests = TaggableConcepts(
    #     verbose_name=_("research interests"),
    #     help_text=_("A list of research interests for the contributor."),
    #     blank=True,
    # )

    links = ArrayField(
        base_field=models.URLField(),
        verbose_name=_("links"),
        help_text=_("A list of online resources related to this contributor."),
        null=True,
        blank=True,
        default=list,
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

    def default_affiliation(self):
        """Returns the default affiliation for the contributor. TODO: make this a foreign key to an organization model."""
        if self.user:
            return self.user.organizations_organization.first()
        return None

    def location(self):
        """Returns the location of the contributor. TODO: make this a foreign key to a location model."""
        return random.choice(["Potsdam", "Adelaide", "Dresden"])
        if self.user:
            return self.user.organization.location
        return None

    def get_absolute_url(self):
        return reverse("contributor-detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("contributor-update", kwargs={"pk": self.pk})

    def profile_image(self):
        if self.image:
            return self.image.url
        return static("img/brand/icon.svg")

    @property
    def type(self):
        if self.user:
            return _("Personal")
        return _("Organizational")

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

    @cached_property
    def owner(self):
        return self.user or self.organization

    @property
    def preferred_email(self):
        if self.user:
            return self.user.email
        return self.organization.owner.user.email


class Identifier(AbstractIdentifier):
    IdentifierLookup = choices.IdentifierLookup
    PERS_ID_TYPES = choices.PersonalIdentifiers
    ORG_ID_TYPES = choices.OrganizationalIdentifiers
    SCHEME_CHOICES = inherited_choices_factory("ContributorIdentifiers", PERS_ID_TYPES, ORG_ID_TYPES)
    scheme = models.CharField(_("scheme"), max_length=32, choices=SCHEME_CHOICES)
    object = models.ForeignKey(to=Contributor, on_delete=models.CASCADE)
