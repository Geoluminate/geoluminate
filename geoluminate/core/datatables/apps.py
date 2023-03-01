from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class DatatablesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "datatables"

    def ready(self):
        from drf_auto_endpoint.router import router

        # if django modeltranslation is installed, make sure that it gets
        # auto-discovered before us
        try:
            from modeltranslation.models import autodiscover

            autodiscover()
        except ImportError:
            pass

        autodiscover_modules("views", register_to=router)
