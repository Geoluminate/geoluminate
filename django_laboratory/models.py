from polymorphic.models import PolymorphicModel
from django.db import models
from django.utils.translation import gettext as _


class Laboratory(models.Model):
    __doc__ = _("A collection/laboratory of scientific instruments.")
    name = models.CharField(max_length=255, verbose_name=_("name"), help_text=_(
        "Name of the laboratory or collection of instruments."))

    class Meta:
        db_table = 'laboratory_laboratory'
        verbose_name = _("laboratory")
        verbose_name_plural = _("laboratories")

    def __str__(self):
        return f"{self.name}"


class Manufacturer(models.Model):
    __doc__ = _("Stores manufacturers of scientific instruments.")
    name = models.CharField(max_length=255, verbose_name=_(
        "name"), help_text=_("Name of the manufacturer."))

    class Meta:
        db_table = 'laboratory_manufacturer'
        verbose_name = _("manufacturer")
        verbose_name_plural = _("manufacturers")

    def __str__(self):
        return f"{self.name}"


class Instrument(PolymorphicModel):
    __doc__ = _("An instrument used for the collection of scientific data.")

    laboratory = models.ForeignKey(
        "django_laboratory.Laboratory",
        verbose_name=_("laboratory"),
        help_text=_("The laboratory to which the instrument belongs."),
        null=True, blank=True,
        on_delete=models.SET_NULL)

    # protected so that deleting a manufacturer will not result in deletion of
    # instruments
    manufacturer = models.ForeignKey(
        'django_laboratory.Manufacturer',
        verbose_name=_("manufacturer"),
        help_text=_("The manufacturer of the instrument."),
        null=True, blank=True,
        on_delete=models.SET_NULL)

    year_manufactured = models.IntegerField(
        verbose_name=_('year manufactured'),
        help_text=_('Year of manufacture of the instrument.'))

    instrument_id = models.CharField(
        max_length=255,
        verbose_name=_("internal ID"),
        help_text=_("Unique internal ID of the instrument. Must be unique for a given instrument type, model and laboratory."))

    model = models.CharField(
        max_length=255,
        verbose_name=_("instrument model"),
        help_text=_("Manufacturer's model of the instrument"))

    type = models.CharField(
        max_length=255,
        verbose_name=_("instrument type"),
        help_text=_("The type of instrument."))

    class Meta:
        db_table = 'laboratory_instrument'
        verbose_name = _("instrument")
        verbose_name_plural = _("instruments")
        unique_together = ('laboratory', 'type', 'model', 'instrument_id')

    def __str__(self):
        return f"{self.name}"
