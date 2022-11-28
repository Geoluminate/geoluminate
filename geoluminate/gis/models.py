from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from django.contrib.gis.db import models
from shortuuid.django_fields import ShortUUIDField
from geoluminate.fields import RangeField
from geoluminate.gis.managers import SiteManager
# from django_extensions.db.fields import ShortUUIDField


class Site(models.Model):
    """The geoluminate site model that all GIS enabled apps should inherit from."""

    objects = SiteManager.as_manager()

    id = ShortUUIDField(
        length=10,
        blank=True,
        max_length=15,
        prefix="GHFS-",
        alphabet="23456789ABCDEFGHJKLMNPQRSTUVWXYZ",
        primary_key=True,
    )
    geom = models.PointField()
    elevation = RangeField(_('elevation (m)'),
                           help_text=_(
                               'elevation with reference to mean sea level (m)'),
                           max_value=9000, min_value=-12000,
                           blank=True, null=True)
    geographic = models.ForeignKey("geoluminate_gis.GeographicLocation",
                                   verbose_name=_('geographic location'),
                                   help_text=_(
                                       'Represents a single country, sea or ocean.'),
                                   blank=True, null=True,
                                   on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Geographic site')
        verbose_name_plural = _('Geographic sites')
        default_related_name = 'site'
        db_table = 'core_gis_site'

    def nearby(self, radius=25):
        """Gets nearby sites within x km radius"""
        point = Point(self.lng, self.lat)
        return self.objects.filter(
            geom__distance_lt=(self.geom, Distance(km=radius)))


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
        ordering = ['name', ]
        verbose_name = _('geographic location')
        verbose_name_plural = _('geographic locations')
        db_table = 'core_gis_geographiclocation'

    def __str__(self):
        return f'{self.name}'
