"""
The utils module contains various helper functions and classes that are used throughout the project.

"""


from allauth.account.forms import LoginForm, SignupForm
from django.apps import apps
from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.utils.module_loading import import_string

# from geoluminate.contrib.core.tests.factories import (
#     DatasetFactory,
#     ProjectFactory,
#     SampleFactory,
# )
from geoluminate.contrib.users.tests.factories import UserFactory


def context_processor(request):
    """A context processor that adds the following variables to the context:

    - ``geoluminate``: The ``GEOLUMINATE`` setting.
    - ``ACCOUNT_ALLOW_REGISTRATION``: The ``ACCOUNT_ALLOW_REGISTRATION`` setting.
    """
    context = {
        "geoluminate": settings.GEOLUMINATE,
        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION,
        "user_sidebar_widgets": settings.GEOLUMINATE_USER_SIDEBAR_WIDGETS,
        "navbar_widgets": settings.GEOLUMINATE_NAVBAR_WIDGETS,
    }
    if not request.user.is_authenticated:
        # get the allauth user login form
        context["login_form"] = LoginForm
        context["register_form"] = SignupForm

    return context


# @transaction.atomic
# def create_fixtures():
#     def save_model_instances(instance_list):
#         for model in instance_list:
#             model.save()

#     # create some users
#     print("Creating users...")
#     save_model_instances(UserFactory.create_batch(size=200))

#     # create some projects
#     print("Creating projects...")
#     save_model_instances(ProjectFactory.create_batch(size=100))

#     # create some datasets
#     print("Creating datasets...")
#     save_model_instances(DatasetFactory.create_batch(size=250))

#     # create some samples
#     print("Creating samples...")
#     save_model_instances(SampleFactory.create_batch(size=1000))


def get_measurement_types():
    """Returns a dictionary of all models in the project that subclass from :class:`geoluminate.contrib.core.models.Measurement`."""
    measurement_types = {}
    Measurement = import_string("geoluminate.contrib.core.models.Measurement")

    for model in apps.get_models():
        if issubclass(model, Measurement):
            measurement_types[model._meta.verbose_name] = model
    return measurement_types


def get_database_models():
    """Get a list of all models in the project that subclass from :class:`geoluminate.models.Base`."""
    db_models = []
    Measurement = import_string("geoluminate.contrib.core.models.Measurement")

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


def geoluminate_content_types():
    """A Q filter for all content types that are part of the Geoluminate database."""
    return Q(app_label__in=[model._meta.app_label for model in get_database_models()])
