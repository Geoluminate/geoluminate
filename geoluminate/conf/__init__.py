"""Default settings for Geoluminate."""
from appconf import AppConf
from django.conf import settings

from .setup import geoluminate_setup

__all__ = ("settings", "GeoluminateConf")


class GeoluminateConf(AppConf):
    """Settings for Geoluminate"""

    BASE_MODEL = "geoluminate.db.models.Base"

    # DATABASES = []

    # DATABASE = None

    DATABASE_NAME = "My Research Database"
    DATABASE_ACRONYM = "MRDB"
    KEYWORDS = ["heat flow", "geothermal", "geoenergy", "renewable energy"]
    GOVERNING_BODY = "International Heat Flow Commission"
    GOVERNING_BODY_ACRONYM = "IHFC"
    GOVERNING_BODY_WEBSITE = "ihfc.org"

    # API_ROUTERS = [
    #     "geoluminate.contrib.gis.urls.router",
    #     "geoluminate.contrib.literature.api.urls.router",
    #     "geoluminate.contrib.literature.api.urls.lit_router",
    # ]

    # GLOSSARY = [
    #     "database.Station",
    #     "database.Run",
    #     "database.TransferFunction",
    # ]
