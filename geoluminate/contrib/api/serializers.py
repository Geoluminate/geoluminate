# import drf_auto_endpoint.metadata.AutoMetadata
# import OpenApiSerializerFieldExtension from drf-spectacular

from django.contrib.gis.db import models
from drf_spectacular.extensions import OpenApiSerializerFieldExtension
from drf_spectacular.plumbing import get_view_model
from quantityfield.settings import DJANGO_PINT_UNIT_REGISTER as ureg
from rest_framework import serializers
from rest_framework_gis.fields import GeometryField

from geoluminate.db import fields


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


class GeoluminateSerializerMixin:
    # class Meta:
    # datatables_always_serialize = ("id",)

    def __init__(self, *args, **kwargs) -> None:
        self.serializer_field_mapping.update(
            {
                fields.QuantityField: QuantityField,
                fields.DecimalQuantityFormField: QuantityField,
                fields.IntegerQuantityField: QuantityField,
                fields.BigIntegerQuantityField: QuantityField,
                fields.PositiveIntegerQuantityField: QuantityField,
                models.PointField: GeometryField,
            }
        )
        super().__init__(*args, **kwargs)


class ModelSerializer(GeoluminateSerializerMixin, serializers.ModelSerializer):
    pass


class HyperlinkedModelSerializer(GeoluminateSerializerMixin, serializers.HyperlinkedModelSerializer):
    pass
