from typing import Any, Optional

from django.conf import settings
from pint import Quantity
from quantityfield import fields
from shortuuid.django_fields import ShortUUIDField


class QuantitityFieldPatch:
    def from_db_value(self, value: Any, *args, **kwargs) -> Optional[Quantity]:
        if value is None:
            return None
        return self.ureg.Quantity(value, getattr(self.ureg, self.base_units))


class QuantityField(QuantitityFieldPatch, fields.QuantityField):
    pass


class DecimalQuantityFormField(QuantitityFieldPatch, fields.DecimalQuantityFormField):
    pass


class IntegerQuantityField(QuantitityFieldPatch, fields.IntegerQuantityField):
    pass


class BigIntegerQuantityField(QuantitityFieldPatch, fields.BigIntegerQuantityField):
    pass


class PositiveIntegerQuantityField(QuantitityFieldPatch, fields.PositiveIntegerQuantityField):
    pass


class PIDField(ShortUUIDField):
    def __init__(self, *args, **kwargs):
        acronym = settings.GEOLUMINATE["database"]["acronym"]

        kwargs["max_length"] = 16
        kwargs["prefix"] = acronym + "-"
        kwargs["length"] = kwargs["max_length"] - len(kwargs["prefix"])
        kwargs["blank"] = True
        kwargs["alphabet"] = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"

        super().__init__(*args, **kwargs)
