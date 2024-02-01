import pprint

from django.apps import AppConfig
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.module_loading import autodiscover_modules
from django.utils.translation import gettext_lazy as _


def update_drf_field_mapping():
    from rest_framework.serializers import ModelSerializer
    from rest_framework_gis.fields import GeometryField

    from geoluminate import models
    from geoluminate.api.fields import QuantityField

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


class GeoluminateConfig(AppConfig):
    name = "geoluminate"
    verbose_name = "Geoluminate"

    def ready(self) -> None:
        # adds a default renderer to all forms to keep a consistent look across the site. This way we don't have to specify it every time
        # patch django-filters to not use crispy forms. should be safe to remove on the
        # next release of geoluminate
        from geoluminate.measurements import measurements
        from geoluminate.utils import get_measurement_models

        autodiscover_modules("plugins")

        from django_filters import compat

        compat.is_crispy = lambda: False

        update_drf_field_mapping()

        # register all measurement models
        for model in get_measurement_models():
            measurements.register(model)

        # pprint.pprint(measurements.registry)

        # settings.SPECTACULAR_SETTINGS["DESCRIPTION"] = render_to_string(
        #     "api/docs/api_description.md", context={"geoluminate": settings.GEOLUMINATE}
        # )

        return super().ready()
