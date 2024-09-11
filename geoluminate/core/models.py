import random

# from rest_framework.authtoken.models import Token
from django.templatetags.static import static
from django.urls import reverse
from django.utils.decorators import classonlymethod
from django.utils.encoding import force_str
from django.utils.functional import cached_property
from django.utils.translation import gettext as _
from polymorphic.models import PolymorphicModel
from polymorphic.showfields import ShowFieldType

from geoluminate.contrib.contributors.managers import ContributionManager
from geoluminate.core import utils
from geoluminate.db import models
from geoluminate.db.fields import PartialDateField
from geoluminate.utils import get_subclasses


def contributor_permissions_default():
    return {"edit": False}


def default_image_path(instance, filename):
    """Returns the path to the image file for the project."""
    # get lowercase plural name of the model
    model_name = instance._meta.verbose_name_plural.replace(" ", "_")

    return f"{model_name}/{instance.pk}/cover.{filename.split('.')[-1]}"


class Abstract(models.Model):
    """An abstract model that contains common fields and methods for both the Project and Dataset models."""

    keywords = models.ManyToManyField(
        "research_vocabs.Concept",
        verbose_name=_("keywords"),
        help_text=_("Controlled keywords for enhanced discoverability"),
        blank=True,
    )

    options = models.JSONField(
        verbose_name=_("options"),
        help_text=_("Item options."),
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
        ordering = ["-modified"]

    def __str__(self):
        return force_str(self.title)

    def is_contributor(self, user):
        """Returns true if the user is a contributor."""

        return self.contributions.filter(contributor=user).exists()

    def get_api_url(self):
        return reverse(f"{type(self).__name__.lower()}-detail", kwargs={"pk": self.pk})

    def get_abstract(self):
        """Returns the abstract description of the project."""
        try:
            return self.descriptions.get(type="Abstract")
        except self.DoesNotExist:
            return None

    def get_meta_description(self):
        abstract = self.get_abstract()
        if abstract:
            return abstract.description
        else:
            return None

    def profile_image(self):
        if self.image:
            return self.image.url
        return static("img/brand/logo.svg")

    def get_meta_image(self):
        return self.profile_image()

    def get_datasets(self):
        return self.datasets.all()

    def get_samples(self):
        return self.samples.all()

    def get_projects(self):
        return self.projects.all()

    def get_metadata_quality(self):
        return random.randint(0, 100)
        # return self.metadata_quality

    def get_data_quality(self):
        return random.randint(0, 100)
        # return self.data_quality

    @cached_property
    def get_descriptions(self):
        descriptions = list(self.descriptions.all())
        # descriptions.sort(key=lambda x: self.DESCRIPTION_TYPES.values.index(x.type))
        return descriptions


class AbstractDescription(models.Model):
    type = ""
    text = models.TextField(_("description"))

    class Meta:
        verbose_name = _("description")
        verbose_name_plural = _("descriptions")
        abstract = True
        default_related_name = "descriptions"
        unique_together = ("object", "type")

    def __str__(self):
        return force_str(self.text)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.type}>"

    def clean(self):
        """Returns description text with p tags stripped"""
        return utils.strip_p_tags(self.text)


class AbstractDate(models.Model):
    type = ""
    date = PartialDateField(_("date"))

    class Meta:
        verbose_name = _("date")
        verbose_name_plural = _("dates")
        abstract = True
        default_related_name = "dates"
        unique_together = ("object", "type")

    def __str__(self):
        return force_str(self.date)

    def __repr__(self):
        return f"<{self.type}: {self.date}>"


class AbstractIdentifier(models.Model):
    """A model for storing generic PIDs."""

    IdentifierLookup = {}
    SCHEME_CHOICES = []
    scheme = None
    object = None
    identifier = models.CharField(_("identifier"), max_length=255, db_index=True)

    class Meta:
        verbose_name = _("identifier")
        verbose_name_plural = _("identifiers")
        unique_together = ["scheme", "identifier"]
        default_related_name = "identifiers"
        abstract = True

    def __str__(self):
        return f"<{self.get_scheme_display()}: {self.identifier}>"

    def URI(self):
        if url := self.IdentifierLookup.get(self.scheme):
            return f"{url}{self.identifier}"


class AbstractContribution(models.Model):
    """A contributor is a person or organisation that has contributed to the project or
    dataset. This model is based on the Datacite schema for contributors."""

    objects = ContributionManager().as_manager()

    CONTRIBUTOR_ROLES = []

    object = None  # must be implemented in subclass
    contributor = models.ForeignKey(
        "contributors.Contributor",
        verbose_name=_("contributor"),
        help_text=_("The person or organisation that contributed to the project or dataset."),
        related_name="%(app_label)s_%(class)ss",
        related_query_name="%(app_label)s_%(class)s",
        null=True,
        on_delete=models.SET_NULL,
    )

    roles = models.JSONField(
        verbose_name=_("roles"),
        help_text=_("Assigned roles for this contributor."),
        default=list,
        null=True,
        blank=True,
    )

    # we can't rely on the contributor field to store necessary information, as the profile may have changed or been deleted, therefore we need to store the contributor's name and other details at the time of publication
    store = models.JSONField(
        _("contributor"),
        help_text=_("A JSON representation of the contributor profile at the time of publication"),
        default=dict,
    )

    # holds the permissions for each contributor, e.g. whether they can edit the object
    permissions = models.JSONField(
        _("permissions"),
        help_text=_("A JSON representation of the contributor's permissions at the time of publication"),
        default=contributor_permissions_default,
    )

    class Meta:
        abstract = True
        verbose_name = _("contributor")
        verbose_name_plural = _("contributors")
        unique_together = ["object", "contributor"]

    def __str__(self):
        return force_str(self.contributor)

    def __repr__(self):
        return f"<{self.contributor}: {self.roles}>"

    def get_absolute_url(self):
        """Returns the absolute url of the contributor's profile."""
        return self.contributor.get_absolute_url()

    def get_update_url(self):
        related_name = self.object._meta.model_name
        letter = related_name[0]
        return reverse("contribution-update", kwargs={"pk": self.object.pk, "model": letter})

    def get_create_url(self):
        related_name = self.object._meta.model_name
        letter = related_name[0]
        return reverse("contribution-create", kwargs={"model": letter, "pk": self.object.pk})

    def profile_to_data(self):
        """Converts the profile to a JSON object."""

        data = {
            "name": self.profile.name,
            "given": self.profile.given,
            "family": self.profile.family,
        }

        ORCID = self.profile.identifiers.filter(scheme="ORCID").first()
        if ORCID:
            data["ORCID"] = ORCID.identifier

        affiliation = self.profile.default_affiliation()
        if affiliation:
            data["affiliation"] = affiliation

        return data


class PolymorphicMixin(ShowFieldType, PolymorphicModel):
    class Meta:
        abstract = True

    @classonlymethod
    def get_subclasses(cls):
        return get_subclasses(cls)

    @classonlymethod
    def get_polymorphic_choices(cls, include_self=False):
        choices = []
        for subclass in cls.get_subclasses():
            opts = subclass._meta
            choices.append((f"{opts.app_label}.{opts.model_name}", opts.verbose_name))
        return choices
