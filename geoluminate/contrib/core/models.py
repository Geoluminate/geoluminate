from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db.models import Collect, Extent
from django.contrib.gis.measure import Distance
from django.core.validators import MaxValueValidator as MaxVal
from django.core.validators import MinValueValidator as MinVal
from django.db import models as django_models
from django.forms.models import model_to_dict
from django.templatetags.static import static
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from multiselectfield.utils import get_max_length
from taggit.managers import TaggableManager

from geoluminate import models
from geoluminate.contrib.core import utils

# from geoluminate.utils.gis.managers import LocationManager
from . import choices


def default_image_path(instance, filename):
    """Returns the path to the image file for the project."""
    # get lowercase plural name of the model
    model_name = instance._meta.verbose_name_plural.replace(" ", "_")

    return f"{model_name}/{instance.uuid}/cover.{filename.split('.')[-1]}"


class Abstract(models.Model):
    """An abstract model that contains common fields and methods for both the Project and Dataset models."""

    DISCOVERY_TAGS = choices.DiscoveryTags

    image = ProcessedImageField(
        verbose_name=_("image"),
        help_text=_("Upload an image that represents your project."),
        processors=[ResizeToFit(1200, 630)],
        format="WEBP",
        options={"quality": 60},
        upload_to=default_image_path,
        blank=True,
        null=True,
        default="world_map.webp",
    )
    title = models.CharField(
        _("name"),
        help_text="The title of the object.",
        max_length=255,
    )
    keywords = TaggableManager(
        verbose_name=_("keywords"), help_text=_("Add keywords to help others discover your work."), blank=True
    )
    tags = models.MultiSelectField(
        choices=DISCOVERY_TAGS,
        max_length=32,
        verbose_name=_("tags"),
        help_text=_("Tags to help others discover your project."),
        blank=True,
        null=True,
    )
    key_dates = GenericRelation(
        "core.KeyDate",
        verbose_name=_("key dates"),
        related_name="%(app_label)ss",
        related_query_name="%(app_label)ss",
        help_text=_("Add some key dates."),
    )
    descriptions = GenericRelation(
        "core.Description",
        verbose_name=_("descriptions"),
        related_name="%(app_label)ss",
        related_query_name="%(app_label)ss",
        help_text=_("Add some descriptions."),
    )
    contributors = GenericRelation(
        "contributors.Contribution",
        verbose_name=_("contributors"),
        related_name="%(app_label)ss",
        related_query_name="%(app_label)ss",
        help_text=_("Add some contributors."),
    )

    funding = models.JSONField(
        verbose_name=_("funding"),
        help_text=_("Include details of any funding received for this project."),
        null=True,
        blank=True,
    )

    # license = License(
    #     help_text=_("Choose an open source license for your project."),
    #     blank=True,
    #     null=True,
    #     on_delete=models.SET_NULL,
    # )

    class Meta:
        abstract = True
        ordering = ["-modified"]

    def __str__(self):
        return force_str(self.title)

    def get_absolute_url(self):
        return reverse(f"core:{type(self).__name__.lower()}-detail", kwargs={"uuid": self.uuid})

    def get_edit_url(self):
        return reverse(f"{type(self).__name__.lower()}-edit", kwargs={"uuid": self.uuid})

    def get_create_url(self):
        return reverse(f"{type(self).__name__.lower()}-add")

    def get_list_url(self):
        return reverse(f"{type(self).__name__.lower()}-list")

    def get_api_url(self):
        return reverse(f"{type(self).__name__.lower()}-detail", kwargs={"uuid": self.uuid})

    def get_abstract(self):
        """Returns the abstract description of the project."""
        try:
            return self.descriptions.get(type=Description.DESCRIPTION_TYPES.ABSTRACT)
        except Description.DoesNotExist:
            return None

    def get_meta_description(self):
        abstract = self.get_abstract()
        if abstract:
            return abstract.description
        else:
            return None

    def get_meta_image(self):
        if self.image:
            return self.image.url
        return static("img/brand/logo.svg")

    def get_datasets(self):
        return self.datasets.all()

    def get_samples(self):
        return self.samples.all()

    def get_projects(self):
        return self.projects.all()

    def get_contact_persons(self):
        """Returns all contributors with the ContactPerson role."""
        return self.contributors.get_contact_persons()


class KeyDate(django_models.Model):
    class DateTypes(models.TextChoices):
        PROPOSED_START = "proposed_start", _("Proposed start")
        PROPOSED_END = "proposed_end", _("Proposed end")
        START = "start", _("Start")
        END = "end", _("End")
        COLLECTION_START = "collection_start", _("Collection start")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    type = models.CharField(
        _("type"),
        help_text=_("The type of date."),
        max_length=255,
        choices=DateTypes.choices,
        default=DateTypes.PROPOSED_START,
    )
    date = models.DateTimeField(_("date"), help_text=_("The date."))

    class Meta:
        verbose_name = _("key date")
        verbose_name_plural = _("key dates")
        ordering = ["date"]
        unique_together = ("type", "content_type", "object_id")
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class Description(django_models.Model):
    # DESCRIPTION_TYPES = datacite.get_choices_for("descriptionType")
    DESCRIPTION_TYPES = choices.DataCiteDescriptionTypes
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    type = models.CharField(
        _("type"),
        max_length=32,
        choices=DESCRIPTION_TYPES.choices,
        default=DESCRIPTION_TYPES.ABSTRACT,
    )
    text = models.TextField(_("description"))
    # content = models.TextField(_("content"))

    class Meta:
        verbose_name = _("description")
        verbose_name_plural = _("descriptions")
        unique_together = ("type", "content_type", "object_id")
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def clean(self):
        """Returns description text with p tags stripped"""
        return utils.strip_p_tags(self.text)


class Identifier(models.Model):
    """A model for storing identifiers for users and organisations."""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    identifier = models.CharField(max_length=255, verbose_name=_("identifier"), unique=True)
    scheme = models.CharField(max_length=255, verbose_name=_("scheme"))

    class Meta:
        verbose_name = _("identifier")
        verbose_name_plural = _("identifiers")
        unique_together = ("content_type", "object_id")
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        return f"<{self.scheme}: {self.identifier}>"
