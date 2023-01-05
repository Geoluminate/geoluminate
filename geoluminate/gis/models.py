from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from django.contrib.gis.db import models
from .base import AbstractSite


class BaseSite(AbstractSite):
    """A concrete base model for GIS enabled databases. 'geoluminate.gis'
    must be in your installed apps to utilize this model in your application.

    .. note:

        Inherit from this class if you plan on working with multiple object types
        for a given site. If you are working with only a single data type, for
        performance reasons you may wish to consider inheriting directly from
        `geoluminate.gis.BaseGIS`.
    """

    class Meta:
        verbose_name = _('Geographic site')
        verbose_name_plural = _('Geographic sites')
        default_related_name = 'site'


class GeographicLocation(models.Model):
    """A multiplygon model that describes geographic locations on Earth.

    TODO: Create a seamless shapefile of countries and
    world oceans that also contains info on other geographic
    features (e.g. continent, etc.)
    """
    mapping = {
        'id': 'OBJECTID',
        'name': 'CONTINENT',
        'poly': 'MULTIPOLYGON',
    }

    slug = AutoSlugField(populate_from='name')

    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=13)
    poly = models.MultiPolygonField(srid=4326)

    class Meta:
        abstract = True
        ordering = ['name', ]
        verbose_name = _('geographic location')
        verbose_name_plural = _('geographic locations')
        db_table = 'core_gis_geographiclocation'

    def __str__(self):
        return f'{self.name}'
