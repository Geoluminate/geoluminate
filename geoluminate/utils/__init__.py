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
    """
    Returns a list of all non-abstract subclasses of the given Django model class.

    Args:
    cls (type): The Django model class to find subclasses of.
    include_self (bool): Whether to include the given class itself in the list.

    Returns:
    list: A list of non-abstract subclasses.
    """
    subclasses = set()

    def recurse(subclass):
        if subclass not in subclasses and not getattr(subclass._meta, "abstract", False):
            subclasses.add(subclass)
            for sub in subclass.__subclasses__():
                recurse(sub)

    recurse(cls)

    if include_self:
        if not getattr(cls._meta, "abstract", False):
            subclasses.add(cls)
    else:
        subclasses.discard(cls)

    return list(subclasses)


def get_sample_models():
    """Returns a dictionary of all models in the project that subclass from :class:`geoluminate.contrib.samples.models.BaseSample`."""
    sample_types = []
    from geoluminate.contrib.samples.models import BaseSample

    for model in apps.get_models():
        if issubclass(model, BaseSample):
            sample_types.append(model)
    return sample_types
