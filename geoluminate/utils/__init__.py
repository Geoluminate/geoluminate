from configuration.models import Configuration
from django.apps import apps
from django.conf import settings
from django_contact_form.forms import ContactForm


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
        "site_config": Configuration.get_solo(),
        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION,
        "user_sidebar_widgets": settings.GEOLUMINATE_USER_SIDEBAR_WIDGETS,
        "navbar_widgets": settings.GEOLUMINATE_NAVBAR_WIDGETS,
        "contact_form": ContactForm(request=request),
    }

    return context


def get_subclasses(model):
    models = apps.get_models()
    return [m for m in models if issubclass(m, model) and m != model]
