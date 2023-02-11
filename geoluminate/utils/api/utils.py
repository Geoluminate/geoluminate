from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string
from rest_framework.routers import SimpleRouter

from geoluminate.conf import settings


def get_api_routers():
    """Get the geoluminate database model defined by `settings.CORE_DATABASE`"""
    router_settings = getattr(settings, "API_ROUTERS")
    routers = []
    for router in router_settings:
        router = import_string(router)
        if not isinstance(router, SimpleRouter):
            raise ImproperlyConfigured(
                "List elements of API_ROUTERS must be a sub class of `rest_framework.routers.SimpleRouter`."
            )
        routers.append(router)
    return routers
