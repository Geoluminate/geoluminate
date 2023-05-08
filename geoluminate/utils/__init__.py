from django.apps import apps
from django.db.models import Q
from django.utils.module_loading import import_string

from geoluminate.conf import settings


def get_database_models():
    """Get a list of all models in the project that subclass from :class:`geoluminate.db.models.Base`."""
    db_models = []
    Geoluminate = import_string("geoluminate.models.Geoluminate")

    for model in apps.get_models():
        if issubclass(model, Geoluminate) and not model.hide_from_api:
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


def geoluminate_content_types():
    """A Q filter for all content types that are part of the Geoluminate database."""
    return Q(app_label__in=[model._meta.app_label for model in get_database_models()])
