from django.db.models import *  # NOQA isort:skip
from django.contrib.gis.db.models import *  # NOQA isort:skip
import uuid
from typing import Iterable, Optional

from django.contrib.gis.db.models import __all__ as models_all
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_bleach.models import BleachField as TextField
from meta.models import ModelMeta
from model_utils import FieldTracker
from multiselectfield import MultiSelectField
from quantityfield.fields import (
    BigIntegerQuantityField,
    DecimalQuantityField,
    IntegerQuantityField,
    PositiveIntegerQuantityField,
    QuantityField,
)

# from geoluminate import models


class Model(ModelMeta, models.Model):
    """Helpful base model that can be used to kickstart your Geoluminate database models with common fields and methods.
    Use like this:

    `from geoluminate import models`
    `class MyModel(models.Model): ...`.

    Inheriting from `geoluminate.models.Model` instead of `django.models.Model` will add the following fields to
    your model:

    created: An automatic datetime field that records when a database entry was created.

    modified: An automatic datetime field that records when a database entry was last modified.

    in addition, this class adds (or allows you to add) the following useful attributes to your model:

    tracker (exists by default) : A `FieldTracker` instance that can be used to track changes to your model instance.

        See: https://django-model-utils.readthedocs.io/en/latest/tracker.html for usage details

    _metadata (must be added yourself): Adding this dictionary to your model will allow the django-meta application to
    populate HTML meta tags from your model fields.

        See: https://django-meta.readthedocs.io/en/latest/models.html#models for usage details
    """

    PRIMARY_DATA_FIELDS: Iterable[str] = []

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="UUID",
        help_text=_("Universally unique identifier for this record."),
    )
    # id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="PID", primary_key=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created", help_text="When this record was created.")
    modified = models.DateTimeField(
        auto_now=True, verbose_name="Modified", help_text="When this record was last modified."
    )

    tracker = FieldTracker()

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return reverse(f"{self._meta.model_name}s:detail", kwargs={"uuid": self.uuid})

    def get_edit_url(self):
        return self.get_absolute_url()
        # return reverse(f"{self._meta.model_name}s:edit", kwargs={"uuid": self.uuid})

    def get_add_url(self):
        return reverse(f"{self._meta.model_name}s:add")

    def get_list_url(self):
        return reverse(f"{self._meta.model_name}s:list")

    def get_api_url(self):
        return reverse(f"api:{self._meta.model_name}:detail", kwargs={"uuid": self.uuid})

    def primary_data_types(self):
        """Return a dictionary of the primary data fields and their values."""
        for field in self.PRIMARY_DATA_FIELDS:
            yield field, getattr(self, field)


__all__ = [
    *models_all,
    "Model",
    "QuantityField",
    "IntegerQuantityField",
    "BigIntegerQuantityField",
    "PositiveIntegerQuantityField",
    "DecimalQuantityField",
    "TextField",
    "MultiSelectField",
]


# class GlobalConfiguration(SingletonModel):
#     site = models.OneToOneField(Site, blank=True, null=True, on_delete=models.SET_NULL)  # type: ignore[var-annotated]
#     logo = FilerImageField(
#         related_name="+",
#         verbose_name=_("Logo"),
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#     )
#     icon = FilerImageField(
#         related_name="+",
#         verbose_name=_("Icon"),
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#     )

#     custodian = models.OneToOneField(
#         to=settings.AUTH_USER_MODEL,
#         limit_choices_to={
#             "is_staff": True,
#         },
#         verbose_name=_("custodian"),
#         related_name="custodian",
#         blank=True,
#         null=True,
#         on_delete=models.SET_NULL,
#     )

#     class Meta:
#         db_table = "global_config"
#         verbose_name = _("Configuration")

#     def __str__(self):
#         return force_str(_("Configuration"))
