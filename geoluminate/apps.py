from django.apps import AppConfig
from django.core.exceptions import ValidationError
from django.utils import formats
from django.utils.translation import gettext_lazy as _


def update_drf_field_mapping():
    from rest_framework.serializers import ModelSerializer
    from rest_framework_gis.fields import GeometryField

    from geoluminate import models
    from geoluminate.api.serializers import QuantityField

    # at the moment we are using the QuantifyField serializer for all QuantityField types
    # however, we will need to update this if we want to support non-readonly models
    ModelSerializer.serializer_field_mapping.update(
        {
            models.QuantityField: QuantityField,
            models.DecimalQuantityField: QuantityField,
            models.IntegerQuantityField: QuantityField,
            models.BigIntegerQuantityField: QuantityField,
            models.PositiveIntegerQuantityField: QuantityField,
            models.PointField: GeometryField,
        }
    )


def from_db_value(self, value, *args, **kwargs):
    if value is None:
        return None
    return self.ureg.Quantity(value, getattr(self.ureg, self.base_units))


def clean(self, value):
    """
    General idea, first try to extract the correct number like done in the other
    classes and then follow the same procedure as in the django default field
    """
    if isinstance(value, list) or isinstance(value, tuple):
        val = value[0]
        units = value[1]
    else:
        # If no multi widget is used
        val = value
        units = self.base_units

    if val in self.empty_values:
        # Make sure the correct functions are called also in case of empty values
        self.validate(None)
        self.run_validators(None)
        return None

    if units not in self.units:
        raise ValidationError(_("%(units)s is not a valid choice") % locals())

    if self.localize:
        val = formats.sanitize_separators(value)

    try:
        val = self.to_number_type(val)
    except (ValueError, TypeError):
        raise ValidationError(self.error_messages["invalid"], code="invalid")

    val = self.ureg.Quantity(val, getattr(self.ureg, units)).to(self.base_units)
    self.validate(val.magnitude)
    self.run_validators(val.magnitude)
    return val


class GeoluminateConfig(AppConfig):
    name = "geoluminate"
    verbose_name = "Geoluminate"

    def ready(self) -> None:
        # adds a default renderer to all forms to keep a consistent look across the site. This way we don't have to specify it every time
        # patch django-filters to not use crispy forms. should be safe to remove on the
        # next release of geoluminate
        from django_filters import compat
        from quantityfield.fields import QuantityFieldMixin, QuantityFormFieldMixin

        QuantityFieldMixin.from_db_value = from_db_value
        QuantityFormFieldMixin.clean = clean

        compat.is_crispy = lambda: False

        update_drf_field_mapping()

        return super().ready()
