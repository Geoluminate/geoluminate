from django.apps import AppConfig


class GisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'geoluminate.gis'
    verbose_name = 'Core GIS'
    label = 'geoluminate_gis'
