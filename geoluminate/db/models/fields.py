from typing import Any, Optional

from django import forms
from django.conf import settings
from django_bleach.models import BleachField
from pint import Quantity
from quantityfield import fields
from quantityfield.fields import QuantityFormFieldMixin
from quantityfield.widgets import QuantityWidget
from shortuuid.django_fields import ShortUUIDField


class QuantityFieldWidget(QuantityWidget):
    template_name = "forms/widgets/quantity_field.html"


class QuantityFormField(QuantityFormFieldMixin, forms.FloatField):
    to_number_type = float

    def __init__(self, *args, **kwargs):
        kwargs.update(
            widget=QuantityFieldWidget,
        )
        super().__init__(*args, **kwargs)
        self.widget = QuantityFieldWidget(base_units=self.base_units, allowed_types=self.units)


class QuantitityFieldPatch:
    def __init__(self, *args, **kwargs):
        self.is_primary_data = kwargs.pop("is_primary_data", False)
        super().__init__(*args, **kwargs)

    def from_db_value(self, value: Any, *args, **kwargs) -> Optional[Quantity]:
        if value is None:
            return None
        return self.ureg.Quantity(value, getattr(self.ureg, self.base_units))


class QuantityField(QuantitityFieldPatch, fields.QuantityField):
    pass


class DecimalQuantityField(QuantitityFieldPatch, fields.DecimalQuantityField):
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


class TextField(BleachField):
    """We are not changing an aspects of BleachField, we are simply redefining it so that users who import from `geoluminate.db.models` will always get a text field that bleaches unwanted HTML. Allowed tags and attributes are defined in `geoluminate/conf/settings/security.py`.
    Overrides can be passed to the field as kwargs. See https://github.com/marksweb/django-bleach for more information.
    """

    pass
