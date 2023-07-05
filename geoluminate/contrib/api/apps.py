from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    label = "geoluminate_api"
    name = "geoluminate.contrib.api"

    def ready(self):
        from geoluminate.api import API

        # if django modeltranslation is installed, make sure that it gets auto-discovered before us
        try:
            from modeltranslation.models import autodiscover

            autodiscover()
        except ImportError:
            pass

        autodiscover_modules("endpoints", register_to=API)
