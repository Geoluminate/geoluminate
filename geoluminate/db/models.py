from django.conf import settings
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from literature.fields import LiteratureM2M
from meta.models import ModelMeta
from model_utils import FieldTracker
from model_utils.models import TimeStampedModel
from polymorphic.models import PolymorphicModel
from shortuuid.django_fields import ShortUUIDField
from simple_history.models import HistoricalRecords

from geoluminate.db.fields import PIDField


class Base(ModelMeta, PolymorphicModel, TimeStampedModel):
    pid = PIDField()
    comment = models.TextField(
        _("comment"),
        help_text=_("General comments regarding the site and/or measurement"),
        blank=True,
        null=True,
    )
    literature = LiteratureM2M(
        help_text=_("Associated literature."),
        blank=True,
    )
    acquired = models.DateTimeField(
        _("date acquired"),
        help_text=_("Date and time of acquisition."),
        null=True,
    )

    tracker = FieldTracker()

    _metadata = {
        "title": "get_meta_title",
        "description": "description",
        "year": "year",
    }

    if not settings.DEBUG:
        history = HistoricalRecords()

    class Meta:
        abstract = True
