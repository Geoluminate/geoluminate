from django.apps import apps
from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.utils.module_loading import import_string

# from geoluminate.factories import SampleFactory, UserFactory
from geoluminate.contrib.project.factories import (
    DatasetFactory,
    ProjectFactory,
    SampleFactory,
)
from geoluminate.contrib.user.factories import UserFactory


@transaction.atomic
def create_fixtures():
    def save_model_instances(instance_list):
        for model in instance_list:
            model.save()

    # create some users
    save_model_instances(UserFactory.create_batch(size=200))

    # create some projects
    save_model_instances(ProjectFactory.create_batch(size=100))

    # create some datasets
    save_model_instances(DatasetFactory.create_batch(size=250))

    # create some samples
    save_model_instances(SampleFactory.create_batch(size=1000))


def get_database_models():
    """Get a list of all models in the project that subclass from :class:`geoluminate.db.models.Base`."""
    db_models = []
    Measurement = import_string("geoluminate.contrib.project.models.Measurement")

    for model in apps.get_models():
        if issubclass(model, Measurement):
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
