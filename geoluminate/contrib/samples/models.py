from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
from django.utils.translation import gettext as _
from easy_thumbnails.fields import ThumbnailerImageField
from polymorphic_treebeard.models import PolymorphicMP_Node
from research_vocabs.fields import ConceptField
from shortuuid.django_fields import ShortUUIDField

from geoluminate.core.models import Abstract, PolymorphicMixin
from geoluminate.core.utils import default_image_path
from geoluminate.db import models

from . import choices
from .choices import SampleStatus


class Sample(Abstract, PolymorphicMixin, PolymorphicMP_Node):
    """A sample is a physical or digital object that is part of a dataset."""

    CONTRIBUTOR_ROLES = choices.SampleRoles
    DESCRIPTION_TYPES = choices.SampleDescriptions()
    # IDENTIFIER_TYPES = choices.DataCiteIdentifiers
    DATE_TYPES = choices.SampleDates()

    id = ShortUUIDField(
        editable=False,
        unique=True,
        prefix="s",
        verbose_name="UUID",
        primary_key=True,
    )
    internal_id = models.CharField(
        _("internal ID"),
        max_length=255,
        help_text=_("An alphanumeric identifier used by the creator/s to identify the sample within a dataset"),
    )
    image = ThumbnailerImageField(
        verbose_name=_("image"),
        blank=True,
        null=True,
        upload_to=default_image_path,
    )
    name = models.CharField(_("name"), max_length=255)
    status = ConceptField(
        verbose_name=_("status"),
        vocabulary=SampleStatus,
        default="unknown",
    )
    options = models.JSONField(
        verbose_name=_("options"),
        help_text=_("Item options."),
        null=True,
        blank=True,
    )

    # GENERIC RELATIONS
    descriptions = GenericRelation("core.Description")
    dates = GenericRelation("core.Date")
    identifiers = GenericRelation("core.Identifier")
    contributors = GenericRelation("contributors.Contribution")

    # RELATIONS
    dataset = models.ForeignKey(
        "datasets.Dataset",
        verbose_name=_("dataset"),
        help_text=_("The dataset for which this sample was collected."),
        related_name="samples",
        on_delete=models.CASCADE,
    )
    keywords = models.ManyToManyField(
        "research_vocabs.Concept",
        verbose_name=_("keywords"),
        help_text=_("Controlled keywords for enhanced discoverability"),
        blank=True,
    )

    class Meta:
        verbose_name = _("sample")
        verbose_name_plural = _("samples")
        ordering = ["created"]
        default_related_name = "samples"

    @staticmethod
    def base_class():
        # this is required for many of the class methods in PolymorphicMixin
        return Sample

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("sample-detail", kwargs={"pk": self.pk})
