from django.conf import settings
from django.contrib import admin
from django.contrib.gis.measure import Distance
from django.core.validators import MaxValueValidator as MaxVal
from django.core.validators import MinValueValidator as MinVal
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from geoluminate import models
from geoluminate.contrib.core.models import Abstract


class Location(models.Model):
    # objects = LocationManager.as_manager()

    name = models.CharField(
        verbose_name=_("name"),
        help_text=_("The name of the location."),
        max_length=255,
        blank=True,
        null=True,
    )
    point = models.PointField(null=True, blank=True)
    polygon = models.PolygonField(null=True, blank=True)
    elevation = models.QuantityField(
        base_units="m",
        unit_choices=["m", "ft"],
        verbose_name=_("elevation"),
        help_text=_("Elevation with reference to mean sea level"),
        validators=[MaxVal(9000), MinVal(-12000)],
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("location")
        verbose_name_plural = _("locations")

    @property
    @admin.display(description=_("latitude"))
    def latitude(self):
        """Convenience method for retrieving the site's latitude ordinate."""
        return self.point.y

    @latitude.setter
    def latitude(self, val):
        self.point.y = val

    @property
    @admin.display(description=_("longitude"))
    def longitude(self):
        """Convenience method for retrieving the site's longitude ordinate."""
        return self.point.x

    @longitude.setter
    def longitude(self, val):
        self.point.x = val

    def __str__(self):
        """Returns the string representation of this site"""
        return f"{self.latitude:.5f}, {self.longitude:.5f}"

    def get_absolute_url(self):
        """Returns the absolute URL for this site"""
        return reverse("location-detail", kwargs={"uuid": self.uuid})

    def get_sites_within(self, radius=25):
        """Gets nearby sites within {radius} km radius"""
        return self.objects.filter(point__distance_lt=(self.point, Distance(km=radius)))


class Sample(Abstract):
    """This model attempts to roughly replicate the schema of the International
    Generic Sample Number (IGSN) registry. Each sample in this table MUST belong to
    a `geoluminate.contrib.datasets.models.Dataset`."""

    # can get more info from www.vocabulary.odsm2
    type = models.CharField(
        choices=[(x, x) for x in settings.GEOLUMINATE_SAMPLE_TYPES],
        verbose_name=_("sample type"),
        default=settings.GEOLUMINATE_DEFAULT_SAMPLE_TYPE,
        help_text=_("The type of sample as per the ODM2 controlled vocabulary."),
        max_length=255,
    )
    description = models.TextField(
        _("description"),
        help_text=_("A description of the sample."),
        blank=True,
        null=True,
    )
    location = models.ForeignKey(
        Location,
        verbose_name=_("location"),
        help_text=_("The location of the sample."),
        related_name="samples",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    comment = models.TextField(
        _("comment"),
        help_text=_("General comments regarding the site and/or measurement"),
        blank=True,
        null=True,
    )

    parent = models.ForeignKey(
        "self", verbose_name=_("parent"), help_text=_("Parent sample"), blank=True, null=True, on_delete=models.CASCADE
    )
    dataset = models.ForeignKey(
        "datasets.Dataset",
        verbose_name=_("dataset"),
        help_text=_("The dataset to which this sample belongs."),
        related_name="samples",
        on_delete=models.CASCADE,
    )

    _metadata = {
        "title": "title",
        "description": "description",
        "type": "research.dataset",
    }

    class Meta:
        verbose_name = _("sample")
        verbose_name_plural = _("samples")
        ordering = ["-modified"]

    # def geojson(self):
    #     from .serializers import SampleGeojsonSerializer

    #     return SampleGeojsonSerializer(self).data


class Measurement(models.Model):
    sample = models.ForeignKey(
        Sample,
        verbose_name=_("sample"),
        help_text=_("The sample on which the measurement was made."),
        on_delete=models.PROTECT,
    )

    class Meta:
        abstract = True
        ordering = ["-modified"]

    @cached_property
    def get_sample(self):
        return self.sample

    @cached_property
    def get_location(self):
        return self.sample.location

    def get_absolute_url(self):
        return self.get_sample.get_absolute_url()
