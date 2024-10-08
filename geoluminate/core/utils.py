import re

from django.apps import apps
from django.conf import settings
from django.db import models
from django.db.models import Manager, TextChoices
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django_contact_form.forms import ContactForm

from geoluminate.identity.models import Authority, Database

# def icon(icon):
#     """Returns the icon for the project."""
#     icon = settings.GEOLUMINATE_ICONS.get(icon, icon)
#     if not icon:
#         raise ValueError(f"Icon {icon} not found in settings.GEOLUMINATE_ICONS.")
#     return icon


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
        "identity": {
            "database": Database.get_solo(),
            "authority": Authority.get_solo(),
        },
        # "site_config": Configuration.get_solo(),
        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION,
        "user_sidebar_widgets": settings.GEOLUMINATE_USER_SIDEBAR_WIDGETS,
        "navbar_widgets": settings.GEOLUMINATE_NAVBAR_WIDGETS,
        "contact_form": ContactForm(request=request),
    }

    return context


def get_subclasses(model):
    models = apps.get_models()
    return [m for m in models if issubclass(m, model) and m != model]


def get_inheritance_chain(model, base_model):
    chain = []
    for base in model.__mro__:
        if hasattr(base, "_meta") and issubclass(base, base_model):
            chain.append(base)
    return chain


def choices_from_qs(qs, field):
    """Return a list of choices from a queryset"""
    return [(k, k) for k in (qs.order_by(field).values_list(field, flat=True).distinct())]


def get_choices(model, field):
    """Return a list of choices from a model"""

    def func():
        return [(k, k) for k in (model.objects.order_by(field).values_list(field, flat=True).distinct())]

    return func


def max_length_from_choices(choices):
    """Return the max length from a list of choices"""
    return max([len(choice[0]) for choice in choices])


def object_from_letter(letter):
    """Return an object from a letter"""
    type_map = {
        "p": "projects.Project",
        "d": "datasets.Dataset",
        "s": "samples.Sample",
    }
    return apps.get_model(type_map.get(letter))


# ascascas


def strip_p_tags(text):
    """Strip <p> tags from a string."""
    return text.replace("</p><p>", "\n").replace("</p>", "").replace("<p>", "")


def generate_xml(dataset):
    """Generate an XML document from a dataset."""
    return render_to_string("publishing/gfz_schema.xml", {"dataset": dataset})


def get_object_media_path(obj):
    """Return the path to an object."""
    return obj._meta.label


def split_camel_case(input_string):
    """Split camel case string into words."""
    words = re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)", input_string)
    return " ".join(words)


def text_choices_factory(name, item_list):
    """Create a TextChoices class from an XMLSchema element."""
    cls_attrs = {}
    for choice in item_list:
        cls_attrs[choice] = (choice, _(split_camel_case(choice)))

    return TextChoices(f"{name}Choices", cls_attrs)


class PublicObjectsManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(visibility=True)
        # return ProjectQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def inactive(self):
        return self.get_queryset().inactive()


def inherited_choices_factory(name, *args):
    """Create a TextChoices class from an XMLSchema element."""
    cls_attrs = {}
    for choice_class in args:
        attrs = {a: getattr(choice_class, a) for a in vars(choice_class) if not a.startswith("_")}
        for key, choice in attrs.items():
            cls_attrs[key] = choice.value, choice.label

    return models.TextChoices(f"{name}Choices", cls_attrs)
