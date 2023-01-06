"""Default settings for Geoluminate."""
from appconf import AppConf
from django.conf import settings

__all__ = ("settings", "GeoluminateConf")


class GeoluminateConf(AppConf):
    """Settings for Geoluminate"""

    BASE_MODEL = 'geoluminate.db.models.Base'

    DATABASES = []

    DATABASE = None

    TABLE = {
        'fields': [
            'get_absolute_url',
            'id',
            'name',
        ]
    }

    API_ROUTERS = [
        'geoluminate.gis.urls.router',
        'literature.api.urls.router',
        'literature.api.urls.lit_router',
    ]

    GLOSSARY = [
        "database.Station",
        "database.Run",
        "database.TransferFunction",
    ]

    class Meta:
        """Prefix for all Geoluminate settings."""
        prefix = "GEOLUMINATE"
