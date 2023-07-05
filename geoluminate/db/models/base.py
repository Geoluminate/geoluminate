from meta.models import ModelMeta
from model_utils import FieldTracker
from model_utils.models import TimeStampedModel


class Model(ModelMeta, TimeStampedModel):
    """Helpful base model that can be used to kickstart your Geoluminate database models with common fields and methods.
    Use like this:

    `from geoluminate.db import models`
    `class MyModel(models.Model): ...`.

    Inheriting from `geoluminate.db.models.Model` instead of `django.db.models.Model` will add the following fields to
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

    tracker = FieldTracker()

    class Meta:
        abstract = True

    def primary_data_types(self):
        """Returns a dictionary of the model's primary data fields and their values."""
        return {
            field.name: self._meta.get_field(field.name)
            for field in self._meta.fields
            if getattr(field, "is_primary_data", False)
        }
