"""Default settings for Geoluminate."""
from appconf import AppConf
from django.conf import settings

__all__ = ("settings", "GeoluminateConf")


class GeoluminateConf(AppConf):
    """Settings for Geoluminate"""

    BASE_MODEL = 'geoluminate.db.models.Base'

    DATABASES = []

    class Meta:
        """Prefix for all Geoluminate settings."""
        prefix = "GEOLUMINATE"
