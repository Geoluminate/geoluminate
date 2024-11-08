from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel
from shortuuid.django_fields import ShortUUIDField

from geoluminate.core.models import PolymorphicMixin
from geoluminate.db import models

from . import choices


class Measurement(models.Model, PolymorphicMixin, PolymorphicModel):
    CONTRIBUTOR_ROLES = choices.MeasurementRoles()
    DESCRIPTION_TYPES = choices.MeasurementDescriptions()
    DATE_TYPES = choices.MeasurementDates()

    id = ShortUUIDField(
        editable=False,
        unique=True,
        prefix="m",
        verbose_name="UUID",
        primary_key=True,
    )

    # GENERIC RELATIONS
    descriptions = GenericRelation("core.Description")
    dates = GenericRelation("core.Date")
    identifiers = GenericRelation("core.Identifier")
    contributors = GenericRelation("contributors.Contribution")

    # RELATIONS
    sample = models.ForeignKey(
        "samples.Sample",
        verbose_name=_("sample"),
        help_text=_("The sample on which the measurement was made."),
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = _("measurement")
        verbose_name_plural = _("measurements")
        ordering = ["-modified"]
        default_related_name = "measurements"

    @staticmethod
    def base_class():
        # this is required for many of the class methods in PolymorphicMixin
        return Measurement

    def get_absolute_url(self):
        return self.sample.get_absolute_url()
