from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from model_utils import FieldTracker
from research_vocabs.fields import ConceptField

from geoluminate.contrib.core.models import AbstractContribution, AbstractDate, AbstractDescription, PolymorphicMixin
from geoluminate.db import models

from . import choices


class Measurement(models.Model, PolymorphicMixin):
    sample = models.ForeignKey(
        "samples.Sample",
        verbose_name=_("sample"),
        help_text=_("The sample on which the measurement was made."),
        on_delete=models.PROTECT,
    )

    contributors = models.ManyToManyField(
        "contributors.Contributor",
        through="measurements.Contribution",
        verbose_name=_("contributors"),
        help_text=_("The contributors to this measurement."),
    )

    tracker = FieldTracker()

    class Meta:
        verbose_name = _("measurement")
        verbose_name_plural = _("measurements")
        ordering = ["-modified"]
        default_related_name = "measurements"

    @cached_property
    def get_location(self):
        return self.sample.location

    def get_absolute_url(self):
        return self.sample.get_absolute_url()


class Description(AbstractDescription):
    type = ConceptField(verbose_name=_("type"), vocabulary=choices.MeasurementDescriptions)
    object = models.ForeignKey(to="measurements.Measurement", on_delete=models.CASCADE)


class Date(AbstractDate):
    type = ConceptField(verbose_name=_("type"), vocabulary=choices.MeasurementDates)
    object = models.ForeignKey(to=Measurement, on_delete=models.CASCADE)


class Contribution(AbstractContribution):
    """A contribution to a project."""

    CONTRIBUTOR_ROLES = choices.MeasurementRoles()

    object = models.ForeignKey(
        "measurements.Measurement",
        on_delete=models.CASCADE,
        related_name="contributions",
        verbose_name=_("measurement"),
    )
    # roles = ArrayField(
    #     base_field=ConceptField(verbose_name=_("type"), vocabulary=CONTRIBUTOR_ROLES),
    #     verbose_name=_("roles"),
    #     help_text=_("Assigned roles for this contributor."),
    #     # size=len(CONTRIBUTOR_ROLES().choices),
    # )
