from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models as django_models
from django.templatetags.static import static
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from taggit.managers import TaggableManager

from geoluminate import models
from geoluminate.contrib.core import utils
from geoluminate.contrib.datasets.choices import DataCiteDescriptionTypes

from . import choices


def default_image_path(instance, filename):
    """Returns the path to the image file for the project."""
    # get lowercase plural name of the model
    model_name = instance._meta.verbose_name_plural.replace(" ", "_")

    return f"{model_name}/{instance.uuid}/cover.{filename.split('.')[-1]}"


class Abstract(models.Model):
    """An abstract model that contains common fields and methods for both the Project and Dataset models."""

    DESCRIPTION_TYPES: list = []
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
    summary = models.CharField(
        _("summary"),
        help_text=_("A short (max 512 characters) plain-language summary."),
        max_length=512,
        blank=True,
        null=True,
    )
    keywords = TaggableManager(
        verbose_name=_("keywords"), help_text=_("Add keywords to help others discover your work."), blank=True
    )
    tags = models.MultiSelectField(
        choices=DISCOVERY_TAGS,
        max_length=32,  # NEEDS TO BE FIXED
        verbose_name=_("tags"),
        help_text=_("Tags to help others discover your project."),
        blank=True,
        null=True,
    )
    key_dates = GenericRelation(
        "core.FuzzyDate",
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
        help_text=_("Related funding information."),
        null=True,
        blank=True,
    )

    options = models.JSONField(
        verbose_name=_("options"),
        help_text=_("Item options."),
        null=True,
        blank=True,
    )

    visibility = models.IntegerField(
        _("visibility"),
        choices=choices.Visibility.choices,
        default=choices.Visibility.PRIVATE,
        help_text=_("Visibility within the application."),
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

    def is_contributor(self, user):
        """Returns true if the user is a contributor."""
        return self.contributors.filter(profile__user=user).exists()

    def has_role(self, user, role):
        """Returns true if the user has the specified role."""
        return self.contributors.by_role(role).filter(profile__user=user).exists()

    def get_api_url(self):
        return reverse(f"{type(self).__name__.lower()}-detail", kwargs={"uuid": self.uuid})

    def get_abstract(self):
        """Returns the abstract description of the project."""
        try:
            return self.descriptions.get(type=self.DESCRIPTION_TYPES.values[0])
        except Description.DoesNotExist:
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

    @cached_property
    def get_contributors(self):
        return list(self.contributors.select_related("profile").all())

    @cached_property
    def get_descriptions(self):
        descriptions = list(self.descriptions.all())
        descriptions.sort(key=lambda x: self.DESCRIPTION_TYPES.values.index(x.type))
        return descriptions


class FuzzyDate(django_models.Model):
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

    year = models.PositiveIntegerField(_("year"), help_text=_("The year."), blank=True, null=True)
    month = models.PositiveIntegerField(_("month"), help_text=_("The month."), blank=True, null=True)
    day = models.PositiveIntegerField(_("day"), help_text=_("The day."), blank=True, null=True)

    class Meta:
        verbose_name = _("key date")
        verbose_name_plural = _("key dates")
        ordering = ["date"]
        unique_together = ("type", "content_type", "object_id")
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class Description(django_models.Model):
    # DESCRIPTION_TYPES = DataCiteDescriptionTypes
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    type = models.CharField(_("type"), max_length=32)
    text = models.TextField(_("description"))

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

    def get_type_display(self):
        choices = self.content_object.DESCRIPTION_TYPES

        type_field = self._meta.get_field("type")
        type_field.choices = choices.choices

        return self._get_FIELD_display(type_field)


class Identifier(models.Model):
    """A model for storing identifiers for users and organisations."""

    URI_LOOKUP = choices.SchemeLookup
    SCHEMES = choices.SchemeChoices

    identifier = models.CharField(max_length=255, verbose_name=_("identifier"), unique=True, db_index=True)
    scheme = models.CharField(
        _("scheme"),
        max_length=255,
        choices=SCHEMES,
    )

    class Meta:
        verbose_name = _("identifier")
        verbose_name_plural = _("identifiers")

    def __str__(self):
        return f"<{self.scheme}: {self.identifier}>"

    @property
    def scheme_uri(self):
        return self.URI_LOOKUP[self.scheme]
