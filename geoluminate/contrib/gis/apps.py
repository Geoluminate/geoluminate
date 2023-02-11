from django.apps import AppConfig


class GisConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "geoluminate.contrib.gis"
    verbose_name = "GIS"
    label = "geoluminate_gis"
