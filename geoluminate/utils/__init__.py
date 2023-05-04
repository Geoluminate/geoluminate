from django.apps import apps
from django.db.models import Q
from django.utils.module_loading import import_string

from geoluminate.conf import settings


def get_database_models():
    """Get a list of all models in the project that subclass from :class:`geoluminate.db.models.Base`."""
    db_models = []
    Geoluminate = import_string("geoluminate.models.Geoluminate")

    for model in apps.get_models():
        if not issubclass(model, Geoluminate) or model._meta.app_label == "geoluminate" or model.hide_from_api:
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
    return settings.GEOLUMINATE["db_name"]


def limit_description_choices():
    """Limit the choices for the description field to models that have a description field."""
    return Q(app_label__in=[model._meta.app_label for model in get_database_models()])
