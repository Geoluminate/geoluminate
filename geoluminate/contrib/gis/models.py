from django.conf import settings
from django.contrib import admin
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
    # point = models.PointField(null=True, blank=True)
    # polygon = models.PolygonField(null=True, blank=True)

    x = models.DecimalField(
        verbose_name=_("x"),
        help_text=_("The x-coordinate of the location."),
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
    )
    y = models.DecimalField(
        verbose_name=_("y"),
        help_text=_("The y-coordinate of the location."),
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
    )

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

    def point2d(self):
        return {"type": "Point", "coordinates": [self.x, self.y]}

    def point3d(self):
        return {"type": "Point", "coordinates": [self.x, self.y, self.elevation]}

    @property
    @admin.display(description=_("latitude"))
    def latitude(self):
        """Convenience method for retrieving the site's latitude ordinate."""
        return self.y

    @latitude.setter
    def latitude(self, val):
        self.y = val

    @property
    @admin.display(description=_("longitude"))
    def longitude(self):
        """Convenience method for retrieving the site's longitude ordinate."""
        return self.x

    @longitude.setter
    def longitude(self, val):
        self.x = val

    def get_absolute_url(self):
        """Returns the absolute URL for this site"""
        return reverse("location-detail", kwargs={"lon": self.longitude, "lat": self.latitude})
