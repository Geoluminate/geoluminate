from django.apps import apps
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.template.loader import render_to_string
from django.utils.text import slugify

from geoluminate.contrib import CORE_MAPPING
from geoluminate.contrib.identity.models import Authority, Database


def label(label):
    """Returns the given label specified in settings.GEOLUMINATE_LABELS."""
    label = settings.GEOLUMINATE_LABELS.get(label)
    if not label:
        raise ValueError(f"settings.GEOLUMINATE_LABELS does not contain a key for '{label}'.")
    return label


def context_processor(request):
    # Get the current site
    current_site = Site.objects.get_current()
    """A context processor that adds the following variables to the context:"""
    context = {
        "config": {
            "site_name": settings.SITE_NAME,
            "site_domain": current_site.domain,
        },
        "identity": {
            "database": Database.get_solo(),
            "authority": Authority.get_solo(),
        },
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


def generate_xml(dataset):
    """Generate an XML document from a dataset."""
    return render_to_string("publishing/gfz_schema.xml", {"dataset": dataset})


def inherited_choices_factory(name, *args):
    """Create a TextChoices class from an XMLSchema element."""
    cls_attrs = {}
    for choice_class in args:
        attrs = {a: getattr(choice_class, a) for a in vars(choice_class) if not a.startswith("_")}
        for key, choice in attrs.items():
            cls_attrs[key] = choice.value, choice.label

    return models.TextChoices(f"{name}Choices", cls_attrs)


def get_model_class(pk):
    """Return a model class from a primary key."""
    return apps.get_model(CORE_MAPPING[pk[0]])


def default_image_path(instance, filename):
    """Generates file paths for images."""
    model_name = slugify(instance._meta.verbose_name_plural)
    return f"{model_name}/{instance.pk}/{filename}"
