from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
from django.utils.decorators import classonlymethod
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel
from polymorphic.showfields import ShowFieldType
from research_vocabs.fields import ConceptField, TaggableConcepts

from geoluminate.contrib.core.models import Abstract, AbstractContribution, AbstractDate, AbstractDescription
from geoluminate.db import models
from geoluminate.utils import get_subclasses

from . import choices
from .choices import FeatureType, SampleStatus, SamplingMedium, SpecimenType

LABELS = settings.GEOLUMINATE_LABELS


class BaseSample(Abstract, ShowFieldType, PolymorphicModel):
    """This model attempts to roughly replicate the schema of the International Generic BaseSample Number (IGSN) registry. Each sample in this table MUST belong to
    a `geoluminate.contrib.datasets.models.Dataset`."""

    parent = models.ForeignKey(
        "self",
        verbose_name=_("parent sample"),
        help_text=_("The sample from which this sample was derived."),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="subsamples",
    )

    name = models.CharField(_("name"), max_length=255)

    status = ConceptField(
        verbose_name=_("status"),
        vocabulary=SampleStatus,
        default="unknown",
    )

    location = models.ForeignKey(
        "gis.Location",
        verbose_name=_("location"),
        help_text=_("The location of the sample."),
        related_name="samples",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
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
    keywords = TaggableConcepts(
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

    _metadata = {
        "title": "name",
    }

    class Meta:
        verbose_name = _(LABELS["sample"]["verbose_name"])
        verbose_name_plural = _(LABELS["sample"]["verbose_name_plural"])
        ordering = ["created"]
        default_related_name = "samples"

    def __str__(self):
        return f"{self.feature_type}: {self.name}"

    def get_absolute_url(self):
        return reverse("sample-detail", kwargs={"pk": self.pk})

    @classonlymethod
    def get_polymorphic_subclasses(cls, include_self=False):
        return get_subclasses(cls, include_self=include_self)

    @classonlymethod
    def get_polymorphic_choices(cls, include_self=False):
        choices = []
        for subclass in cls.get_polymorphic_subclasses(include_self=include_self):
            opts = subclass._meta
            choices.append((f"{opts.app_label}.{opts.model_name}", opts.verbose_name))
        return choices


class Sample(BaseSample):
    feature_type = ConceptField(
        verbose_name=_("feature"),
        vocabulary=FeatureType,
        default=settings.GEOLUMINATE_DEFAULT_FEATURE_TYPE,
    )
    medium = ConceptField(
        verbose_name=_("medium"),
        vocabulary=SamplingMedium,
        default="solid",
    )
    specimen_type = ConceptField(
        verbose_name=_("specimen"),
        vocabulary=SpecimenType,
        default="theSpecimenTypeIsUnknown",
    )

    class Meta:
        abstract = True


class Description(AbstractDescription):
    type = ConceptField(verbose_name=_("type"), vocabulary=choices.SampleDescriptions)
    object = models.ForeignKey(to=BaseSample, on_delete=models.CASCADE)


class Date(AbstractDate):
    type = ConceptField(verbose_name=_("type"), vocabulary=choices.SampleDates)
    object = models.ForeignKey(to=BaseSample, on_delete=models.CASCADE)


class Contribution(AbstractContribution):
    """A contribution to a project."""

    CONTRIBUTOR_ROLES = choices.SampleRoles

    object = models.ForeignKey(
        BaseSample,
        on_delete=models.CASCADE,
        related_name="contributions",
        verbose_name=_("sample"),
    )
    roles = ArrayField(
        models.CharField(
            max_length=len(max(CONTRIBUTOR_ROLES.values, key=len)),
            choices=CONTRIBUTOR_ROLES.choices,
        ),
        verbose_name=_("roles"),
        help_text=_("Assigned roles for this contributor."),
        size=len(CONTRIBUTOR_ROLES.choices),
    )
