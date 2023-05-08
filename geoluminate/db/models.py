from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from literature.fields import LiteratureM2M
from meta.models import ModelMeta
from model_utils import FieldTracker
from model_utils.models import TimeStampedModel

from geoluminate.contrib.gis.managers import SiteManager
from geoluminate.db.fields import PIDField, RangeField


class Base(ModelMeta, TimeStampedModel):
    objects = SiteManager.as_manager()

    pid = PIDField()

    IGSN = models.IntegerField(
        "IGSN",
        help_text=_("An International Generic Sample Number for the site."),
        blank=True,
        null=True,
    )

    name = models.CharField(
        verbose_name=_("name"),
        null=True,
        help_text=_("Specified site name for the related database entry"),
        max_length=255,
    )

    geom = models.PointField(null=True, blank=True)

    elevation = RangeField(
        _("elevation (m)"),
        help_text=_("elevation with reference to mean sea level (m)"),
        max_value=9000,
        min_value=-12000,
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

    comment = models.TextField(
        _("comment"),
        help_text=_("General comments regarding the site and/or measurement"),
        blank=True,
        null=True,
    )

    tracker = FieldTracker()

    _metadata = {
        "title": "get_meta_title",
        "description": "description",
        "year": "year",
    }

    # if not settings.DEBUG:
    # history = HistoricalRecords()

    class Meta:
        abstract = True
        permissions = [
            (
                "geoluminate_database_admin",
                _("Can create, view, update or delete any model associated with the research database"),
            ),
        ]
