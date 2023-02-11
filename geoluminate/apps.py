from django.apps import AppConfig
from drf_auto_endpoint.endpoints import BaseEndpoint

# BaseEndpoint.as_view = None


class GeoluminateConfig(AppConfig):
    name = "geoluminate"
    verbose_name = "Geoluminate"

    def ready(self) -> None:
        import jazzmin.templatetags
        import jazzmin.utils

        from geoluminate.contrib.admin import monkeypatch

        jazzmin.utils.make_menu = monkeypatch.make_menu
        # setattr(jazzmin.utils, "make_menu", monkeypatch.make_menu)
        return super().ready()
