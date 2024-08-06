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
        "geoluminate": settings.GEOLUMINATE,
        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION,
        "user_sidebar_widgets": settings.GEOLUMINATE_USER_SIDEBAR_WIDGETS,
        "navbar_widgets": settings.GEOLUMINATE_NAVBAR_WIDGETS,
        "contact_form": ContactForm(request=request),
    }

    return context


def get_subclasses(cls, include_self=False):
    """Returns a list of all subclasses of the given class."""
    subclasses = []
    for subclass in cls.__subclasses__():
        subclasses.append(subclass)
        subclasses.extend(get_subclasses(subclass))
    if include_self:
        subclasses.append(cls)
    return subclasses


def get_sample_models():
    """Returns a dictionary of all models in the project that subclass from :class:`geoluminate.contrib.samples.models.Sample`."""
    sample_types = []
    from geoluminate.contrib.samples.models import Sample

    for model in apps.get_models():
        if issubclass(model, Sample):
            sample_types.append(model)
    return sample_types
