from allauth.account.forms import LoginForm, SignupForm
from django.apps import apps
from django.conf import settings
from django.db.models import Q
from django.utils.module_loading import import_string
from django_contact_form.forms import ContactForm

from geoluminate.models import Dataset


def icon(icon):
    """Returns the icon for the project."""
    icon = settings.GEOLUMINATE_ICONS.get(icon, icon)
    if not icon:
        raise ValueError(f"Icon {icon} not found in settings.GEOLUMINATE_ICONS.")
    return icon


def label(label):
    """Returns the given label specified in settings.GEOLUMINATE_LABELS."""
    label = settings.GEOLUMINATE_LABELS.get(label)
    if not label:
        raise ValueError(f"settings.GEOLUMINATE_LABELS does not contain a key for '{label}'.")
    return label


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
        "contact_form": ContactForm(request=request),
        # REMOVE THIS, TESTING ONLY
        "dataset": Dataset.objects.first(),
    }
    if not request.user.is_authenticated:
        # get the allauth user login form
        context["login_form"] = LoginForm
        context["register_form"] = SignupForm

    return context


def get_measurement_models():
    """Returns a dictionary of all models in the project that subclass from :class:`geoluminate.contrib.core.models.Measurement`."""
    measurement_types = []
    Measurement = import_string("geoluminate.contrib.samples.models.Measurement")

    for model in apps.get_models():
        if issubclass(model, Measurement):
            measurement_types.append(model)
    return measurement_types


def geoluminate_content_types():
    """A Q filter for all content types that are part of the Geoluminate database."""
    return Q(app_label__in=[model._meta.app_label for model in get_measurement_models()])
