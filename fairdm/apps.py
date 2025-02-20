from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class FairDMConfig(AppConfig):
    name = "fairdm"

    def ready(self) -> None:
        # adds a default renderer to all forms to keep a consistent look across the site. This way we don't have to specify it every time
        # patch django-filters to not use crispy forms. should be safe to remove on the
        # next release of fairdm

        autodiscover_modules("plugins")
        autodiscover_modules("config")

        from django_filters import compat

        compat.is_crispy = lambda: False

        self.update_drf_field_mapping()

        return super().ready()

    def update_drf_field_mapping(self):
        """
        Updates the default field mapping of Django Rest Framework's ModelSerializer to include proper serializers for
        some of the custom model fields included in FairDM. Doing this means that we don't have to specify the
        serializer for these fields every time we create a new serializer.

        Note: At the moment, `QuantityField` serializer is used for all `QuantityField` types. However, this will need to be updated if non-readonly models are to be supported.

        This function is called during the `FairDMConfig.ready` method.
        """

        from rest_framework.serializers import ModelSerializer

        from fairdm.contrib.api.fields import QuantityField
        from fairdm.db import models

        # if settings.GIS_ENABLED:
        #     from django.contrib.gis.db import models as gis_models
        #     from rest_framework_gis.fields import GeometryField

        #     ModelSerializer.serializer_field_mapping.update(
        #         {
        #             gis_models.PointField: GeometryField,
        #         }
        #     )

        # at the moment we are using the QuantifyField serializer for all QuantityField types
        # however, we will need to update this if we want to support non-readonly models
        ModelSerializer.serializer_field_mapping.update(
            {
                models.QuantityField: QuantityField,
                models.DecimalQuantityField: QuantityField,
                models.IntegerQuantityField: QuantityField,
                models.BigIntegerQuantityField: QuantityField,
                models.PositiveIntegerQuantityField: QuantityField,
            }
        )
