from django.conf import settings

# from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.utils.translation import gettext as _
from polymorphic_treebeard.models import PolymorphicMP_Node
from research_vocabs.fields import ConceptField
from shortuuid.django_fields import ShortUUIDField

from geoluminate.core.models import (
    Abstract,
    AbstractContribution,
    AbstractDate,
    AbstractDescription,
    PolymorphicMixin,
)
from geoluminate.db import models

from . import choices
from .choices import SampleStatus

LABELS = settings.GEOLUMINATE_LABELS


class Sample(Abstract, PolymorphicMixin, PolymorphicMP_Node):
    """This model attempts to roughly replicate the schema of the International Generic Sample Number (IGSN) registry. Each sample in this table MUST belong to
    a `geoluminate.contrib.datasets.models.Dataset`."""

    # _metadata = Metadata()

    id = ShortUUIDField(
        editable=False,
        unique=True,
        prefix="p",
        verbose_name="UUID",
        primary_key=True,
    )

    internal_id = models.CharField(
        _("internal ID"),
        max_length=255,
        help_text=_("An alphanumeric identifier used by the creator/s to identify the sample within a dataset"),
    )

    name = models.CharField(_("name"), max_length=255)

    status = ConceptField(
        verbose_name=_("status"),
        vocabulary=SampleStatus,
        default="unknown",
    )

    dataset = models.ForeignKey(
        "datasets.Dataset",
        verbose_name=_("dataset"),
        help_text=_("The dataset for which this sample was collected."),
        related_name="samples",
        on_delete=models.CASCADE,
    )

    contributors = models.ManyToManyField(
        "contributors.Contributor",
        through="samples.Contribution",
        verbose_name=_("contributors"),
        help_text=_("The contributors to this sample."),
        blank=True,
    )

    options = models.JSONField(
        verbose_name=_("options"),
        help_text=_("Item options."),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _(LABELS["sample"]["verbose_name"])
        verbose_name_plural = _(LABELS["sample"]["verbose_name_plural"])
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


class Description(AbstractDescription):
    type = ConceptField(verbose_name=_("type"), vocabulary=choices.SampleDescriptions)
    object = models.ForeignKey(to=Sample, on_delete=models.CASCADE)


class Date(AbstractDate):
    type = ConceptField(verbose_name=_("type"), vocabulary=choices.SampleDates)
    object = models.ForeignKey(to=Sample, on_delete=models.CASCADE)


class Contribution(AbstractContribution):
    """A contribution to a project."""

    CONTRIBUTOR_ROLES = choices.SampleRoles

    object = models.ForeignKey(
        Sample,
        on_delete=models.CASCADE,
        related_name="contributions",
        verbose_name=_("sample"),
    )
    # roles = ArrayField(
    #     models.CharField(
    #         max_length=len(max(CONTRIBUTOR_ROLES.values, key=len)),
    #         choices=CONTRIBUTOR_ROLES.choices,
    #     ),
    #     verbose_name=_("roles"),
    #     help_text=_("Assigned roles for this contributor."),
    #     size=len(CONTRIBUTOR_ROLES.choices),
    # )
