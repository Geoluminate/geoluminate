from decimal import Decimal

from django.db import models
from partial_date import PartialDateField as BasePartialDateField
from quantityfield import fields

from fairdm.forms import PartialDateFormField


class BigIntegerQuantityField(fields.BigIntegerQuantityField):
    to_number_type = int

    def formfield(self, **kwargs):
        return models.BigIntegerField.formfield(self, **kwargs)


class DecimalQuantityField(fields.DecimalQuantityField):
    to_number_type = Decimal

    def formfield(self, **kwargs):
        return models.DecimalField.formfield(self, **kwargs)


class IntegerQuantityField(fields.IntegerQuantityField):
    to_number_type = int

    def formfield(self, **kwargs):
        return models.IntegerField.formfield(self, **kwargs)


class PositiveIntegerQuantityField(fields.PositiveIntegerQuantityField):
    to_number_type = int

    def formfield(self, **kwargs):
        return models.PositiveIntegerField.formfield(self, **kwargs)


class QuantityField(fields.QuantityField):
    to_number_type = float

    def formfield(self, **kwargs):
        return models.FloatField.formfield(self, **kwargs)


class PartialDateField(BasePartialDateField):
    def formfield(self, **kwargs):
        # Specify the form field to use for this model field
        defaults = {"form_class": PartialDateFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)
