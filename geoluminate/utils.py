import importlib
from geoluminate.conf import settings
from rest_framework.routers import SimpleRouter
from django.core.exceptions import ImproperlyConfigured
from django.apps import apps
from django.db import models
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _


def choices_from_qs(qs, field):
    return [(k, k) for k in (qs.order_by(field)
                             .values_list(field, flat=True).
                             distinct())]


def get_choices(model, field):
    def func():
        return [(k, k) for k in (model.objects.order_by(field)
                                 .values_list(field, flat=True).
                                 distinct())]
    return func


def import_attribute(path):
    assert isinstance(path, str)
    pkg, attr = path.rsplit(".", 1)
    ret = getattr(importlib.import_module(pkg), attr)
    return ret


def get_core_database():
    """Fetches the geoluminate database model defined by `settings.CORE_DATABASE`"""
    return getattr(settings, 'GEOLUMINATE_DATABASE', None)


def get_api_routers():
    """Get the geoluminate database model defined by `settings.CORE_DATABASE`"""
    router_settings = getattr(settings, 'GEOLUMINATE_API_ROUTERS')
    routers = []
    for router in router_settings:
        router = import_attribute(router)
        if not isinstance(router, SimpleRouter):
            raise ImproperlyConfigured(
                'List elements of GEOLUMINATE_API_ROUTERS must be a sub class of `rest_framework.routers.SimpleRouter`.')
        routers.append(router)
    return routers


def get_form_class(forms, form_id, default_form):
    form_class = forms.get(form_id, default_form)
    if isinstance(form_class, str):
        form_class = import_attribute(form_class)
    return form_class


def get_db_name():
    return _(getattr(settings, 'SITE_NAME'))


db_string = get_core_database()
if db_string:
    DATABASE = apps.get_model(get_core_database())
    db_name = DATABASE._meta.verbose_name
else:
    DATABASE = models.Model
    db_name = 'undefined'
