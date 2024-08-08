from django.conf import settings
from django.contrib import admin
from django.contrib.gis.measure import Distance
from django.core.validators import MaxValueValidator as MaxVal
from django.core.validators import MinValueValidator as MinVal
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from geoluminate.db import models

LABELS = settings.GEOLUMINATE_LABELS


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

    def __str__(self):
        """Returns the string representation of this site"""
        return f"{self.latitude}, {self.longitude}"

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

    def get_absolute_url(self):
        """Returns the absolute URL for this site"""
        return reverse("location-detail", kwargs={"lon": self.longitude, "lat": self.latitude})

    def get_sites_within(self, radius=25):
        """Gets nearby sites within {radius} km radius"""
        return self.objects.filter(point__distance_lt=(self.point, Distance(km=radius)))
