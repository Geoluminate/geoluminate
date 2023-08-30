from drf_spectacular.extensions import OpenApiSerializerFieldExtension
from drf_spectacular.plumbing import get_view_model
from quantityfield.settings import DJANGO_PINT_UNIT_REGISTER as ureg
from rest_framework import serializers


class QuantityFieldFix(OpenApiSerializerFieldExtension):
    target_class = "geoluminate.contrib.api.serializers.QuantityField"

    def map_serializer_field(self, auto_schema, direction):
        base = auto_schema._map_serializer_field(self.target, direction, bypass_extensions=True)
        model = get_view_model(auto_schema.view, emit_warnings=False)

        if model is not None:
            field = model._meta.get_field(self.target.source_attrs[0])
        base["units"] = field.base_units
        # base["accepted_units"] = field.unit_choices
        return base


class QuantityJSONField(serializers.FloatField):
    def to_representation(self, value):
        return {"magnitude": value.magnitude, "unit": f"{value.units}"}

    def to_internal_value(self, data):
        return ureg.Quantity(data["magnitude"], data["unit"])


class QuantityField(serializers.FloatField):
    def __init__(self, *args, **kwargs):
        # print(args, kwargs)
        return super().__init__(*args, **kwargs)

    def to_representation(self, value):
        return value.magnitude
