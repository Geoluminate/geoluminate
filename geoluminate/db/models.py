from django.db.models import *  # isort:skip

from django.db import models
from django.urls import reverse
from django_bleach.models import BleachField as TextField
from django_filters import FilterSet
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

    class Meta:
        abstract = True

    class Config:
        metadata: Metadata = None
        filterset_class: FilterSet = None
        filterset_fields: list = []
        serializer_class = None
        serializer_fields: list = []

    def get_absolute_url(self):
        return reverse(f"{self._meta.model_name}-detail", kwargs={"pk": self.pk})


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
