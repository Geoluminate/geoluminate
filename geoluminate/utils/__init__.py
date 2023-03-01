from django.apps import apps

from geoluminate.conf import settings
from geoluminate.db.models import Base
from geoluminate.models import Geoluminate


def get_database_models():
    """Get a list of all models in the project that subclass from :class:`geoluminate.db.models.Base`."""
    db_models = []
    for model in apps.get_models():
        if (
            not issubclass(model, Base)
            or model is Geoluminate
            or getattr(model, "hide_from_api")
        ):
            continue

        db_models.append(model)
    return db_models


def get_filter_params(request):
    """Returns curent filter params as a string"""
    params = request.GET.copy()
    params.pop("page", True)
    if params:
        return "&" + params.urlencode()
    else:
        return ""


def get_db_name():
    return getattr(settings, "DATABASE_NAME")
