from django.db.models import *  # isort:skip

from django.db import models
from django.urls import reverse
from django_bleach.models import BleachField as TextField
from model_utils import FieldTracker

from .fields import (
    BigIntegerQuantityField,
    DecimalQuantityField,
    IntegerQuantityField,
    PositiveIntegerQuantityField,
    QuantityField,
)


class FairDMOptions:
    """
    A class to handle verification of the attributes declared in the FairDM inner class.
    Similar to Django's `Options` class.
    """

    def __init__(self, fairdm):
        self.fairdm = fairdm

    def validate(self):
        """
        Add custom validation for FairDM attributes here.
        Example: Check if necessary fields are present or if the data structure is correct.
        """
        # Example validation: Ensure 'metadata' is a dictionary
        if not isinstance(self.fairdm.metadata, dict):
            raise ValueError("FairDM metadata must be a dictionary.")

        # Add more validation logic as needed
        # Example: Ensure 'fields' is a list
        if not isinstance(self.fairdm.fields, list):
            raise ValueError("FairDM fields must be a list.")


class FairDM(models.base.ModelBase):
    """
    Metaclass that merges FairDM inner classes of parent classes into the current class.
    It subclasses ModelBase to ensure Django's native model functionality remains intact.
    """

    def __new__(cls, name, bases, attrs):
        # Check if any parent class inherits from FairDM
        parents = [b for b in bases if isinstance(b, FairDM)]

        if not parents:
            # If no parent class inherits from FairDM, use the default behavior
            return super().__new__(cls, name, bases, attrs)

        # Pop the FairDM attribute before creating new_class
        fairdm = attrs.pop("FairDM", None)

        # Create the new class
        new_class = super().__new__(cls, name, bases, attrs)

        # Add the FairDMOptions instance to the new class
        if fairdm:
            # Create an instance of FairDMOptions and add it to the class
            options = FairDMOptions(fairdm)
            new_class.add_to_class("_fairdm", options)

            # Validate the FairDM attributes
            options.validate()

        return new_class


class Model(models.Model, metaclass=FairDM):
    """Helpful base model that can be used to kickstart your FairDM database models with common fields and methods.
    Use like this:

    `from fairdm.db import models`
    `class MyModel(models.Model): ...`.

    Inheriting from `fairdm.models.Model` instead of `django.models.Model` will add the following fields to
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
