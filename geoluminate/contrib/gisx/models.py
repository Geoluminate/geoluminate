from django.contrib.gis.db import models
from django.utils.translation import gettext as _


class Country(models.Model):
    source = "https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-countries/"

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
