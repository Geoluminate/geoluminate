from django.db.models import *  # isort:skip

# from django.contrib.gis.db.models import *  # isort:skip

# from django.contrib.gis.db.models import __all__ as models_all
from django.db import models
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django_bleach.models import BleachField as TextField
from model_utils import FieldTracker
from quantityfield.fields import (
    BigIntegerQuantityField,
    DecimalQuantityField,
    IntegerQuantityField,
    PositiveIntegerQuantityField,
    QuantityField,
)

from geoluminate.metadata import Metadata


class Model(models.Model):
    """Helpful base model that can be used to kickstart your Geoluminate database models with common fields and methods.
    Use like this:

    `from geoluminate.db import models`
    `class MyModel(models.Model): ...`.

    Inheriting from `geoluminate.models.Model` instead of `django.models.Model` will add the following fields to
    your model:

    created: An automatic datetime field that records when a database entry was created.

    modified: An automatic datetime field that records when a database entry was last modified.

    in addition, this class adds (or allows you to add) the following useful attributes to your model:

    tracker (exists by default) : A `FieldTracker` instance that can be used to track changes to your model instance.

        See: https://django-model-utils.readthedocs.io/en/latest/tracker.html for usage details


        See: https://django-meta.readthedocs.io/en/latest/models.html#models for usage details
    """

    # id = models.UUIDField(
    #     default=uuid.uuid4,
    #     editable=False,
    #     unique=True,
    #     verbose_name="UUID",
    #     primary_key=True,
    # )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created",
        help_text="When this record was created.",
    )
    modified = models.DateTimeField(
        auto_now=True,
        verbose_name="Modified",
        help_text="When this record was last modified.",
    )

    tracker = FieldTracker()

    _metadata: Metadata = None

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return reverse(f"{self._meta.model_name}-detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse(f"{self._meta.model_name}-update", kwargs={"pk": self.pk})
        # return self.get_absolute_url()
        # return reverse(f"{self._meta.model_name}s:edit", kwargs={"pk": self.pk})

    def get_add_url(self):
        return reverse(f"{self._meta.model_name}-create")

    def get_list_url(self):
        return reverse(f"{self._meta.model_name}-list")

    def get_api_url(self):
        return reverse(f"api:{self._meta.model_name}-detail", kwargs={"pk": self.pk})

    def get_absolute_url_link(self):
        string = escape(str(self))
        return mark_safe(f"<a href='{self.get_absolute_url()}'>{string}</a>")

    __html__ = get_absolute_url_link


__all__ = [
    # *models_all,
    "Model",
    "QuantityField",
    "IntegerQuantityField",
    "BigIntegerQuantityField",
    "PositiveIntegerQuantityField",
    "DecimalQuantityField",
    "TextField",
]
