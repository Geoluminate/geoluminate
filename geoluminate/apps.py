from django.apps import AppConfig
from drf_auto_endpoint.endpoints import BaseEndpoint

# BaseEndpoint.as_view = None


class GeoLuminateConfig(AppConfig):
    name = 'geoluminate'
    verbose_name = 'GeoLuminate'
