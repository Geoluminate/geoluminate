from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from geoluminate.contrib.project.models import Sample

from .managers import SiteManager


class Site(Sample):
    objects = SiteManager.as_manager()

    class Meta:
        verbose_name = _("Site")
        verbose_name_plural = _("Sites")
        proxy = True

    @property
    def latitude(self):
        """Convenience method for retrieving the site's latitude ordinate.

        Returns:
            Float: the site latitude
        """
        return self.geom.y

    @latitude.setter
    def latitude(self, val):
        self.geom.y = val

    @property
    def longitude(self):
        """Convenience method for retrieving the site's longitude ordinate.

        Returns:
            Float: the site longitude
        """
        return self.geom.x

    @longitude.setter
    def longitude(self, val):
        self.geom.x = val

    @property
    def lon(self):
        """Alias of self.longitude"""
        return self.longitude

    @lon.setter
    def lon(self, val):
        self.geom.x = val

    @property
    def lat(self):
        """Alias of self.latitude"""
        return self.latitude

    @lat.setter
    def lat(self, val):
        self.geom.y = val

    def __str__(self):
        """Returns the string representation of this site"""
        return f"{self.lat}, {self.lon}"

    def get_absolute_url(self):
        """Returns the absolute URL for this site"""
        return reverse("site", kwargs={"pk": self.pk})

    def get_sites_within(self, radius=25):
        """Gets nearby sites within {radius} km radius"""
        return self.objects.filter(geom__distance_lt=(self.geom, Distance(km=radius)))

    def to_UTM(self):
        """Converts site coordinates to UTM. Not implemented yet."""
        pass
