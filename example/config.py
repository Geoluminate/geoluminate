from django.utils.translation import gettext_lazy as _

import fairdm
from fairdm.contrib.import_export.resources import MeasurementResource, SampleResource
from fairdm.core.tables import MeasurementTable, SampleTable
from fairdm.metadata import Authority, Citation, ModelConfig

from .filters import CustomSampleFilter
from .models import CustomParentSample, CustomSample, ExampleMeasurement
from .tables import CustomSampleTable


class ExampleBaseConfig(ModelConfig):
    authority = Authority(
        name=_("FairDM Core Development"),
        short_name="FairDM",
        website="https://fairdm.org",
    )
    citation = Citation(
        text="FairDM Core Development Team (2021). FairDM: A FAIR Data Management Tool. https://fairdm.org",
        doi="https://doi.org/10.5281/zenodo.123456",
    )
    repository_url = "https://github.com/FAIR-DM/fairdm"


@fairdm.register(CustomParentSample)
class CustomParentSampleConfig(ExampleBaseConfig):
    description = "A rock sample is a naturally occurring solid material that is composed of one or more minerals or mineraloids and represents a fragment of a larger geological formation or rock unit. The sample is typically obtained from a specific location in order to study its physical properties, mineral composition, texture, structure, and formation processes."
    keywords = []
    filterset_options = {"fields": ["name", "char_field"]}
    # filterset_class = "example.filters.SampleFilter"
    fields = [
        ("name", "status"),
        "char_field",
        ("created", "modified"),
    ]
    resource_class = SampleResource
    table_class = SampleTable
    # fieldsets = {
    #     None: {
    #         "fields": (
    #             ("name", "status"),
    #             "char_field",
    #         ),
    #     }
    # }


@fairdm.register(CustomSample)
class CustomSampleConfig(ExampleBaseConfig):
    primary_data_fields = ["char_field"]
    description = "A thin section is a small, flat slice of rock, mineral, or other material that has been carefully ground and polished to a standard thickness, typically around 30 micrometers (0.03 millimeters). This thinness allows light to pass through the sample when viewed under a polarizing light microscope. Thin sections are used in petrography (the study of rocks) and mineralogy to examine the optical properties, texture, and microstructure of the sample, which helps in identifying the minerals present, understanding the rock's formation history, and determining its geological significance."
    keywords = []
    filterset_class = CustomSampleFilter
    table_class = CustomSampleTable
    fieldsets = {
        None: {
            "fields": (
                ("name", "status"),
                ("created", "modified"),
                "boolean_field",
            ),
        },
        "Text-based fields": {
            "description": "This section demonstrates how text fields are rendered",
            "fields": ("char_field", "text_field"),
        },
        "Numeric fields": {
            "description": "This section demonstrates how numeric fields are rendered",
            "fields": (
                ("integer_field", "big_integer_field", "small_integer_field"),
                ("positive_integer_field", "positive_small_integer_field"),
                ("float_field", "decimal_field"),
            ),
        },
        "Date/Time fields": {
            "description": "This section demonstrates how date/time fields are rendered",
            "fields": (("date_field", "time_field", "date_time_field")),
        },
    }
    non_editable_fields = ["created"]

    fields = [
        "name",
        "char_field",
        "text_field",
        "integer_field",
        "big_integer_field",
        "positive_integer_field",
        "positive_small_integer_field",
        "small_integer_field",
        "boolean_field",
        "date_field",
        "date_time_field",
        "time_field",
        "decimal_field",
        "float_field",
    ]


@fairdm.register(ExampleMeasurement)
class ExampleMeasurementConfig(ExampleBaseConfig):
    primary_data_fields = ["char_field"]
    description = "An example measurement"
    filterset_options = {"fields": ["name", "char_field"]}
    resource_class = MeasurementResource
    table_class = MeasurementTable
    fields = [
        "sample",
        "name",
        "char_field",
        "text_field",
        "integer_field",
        "big_integer_field",
        "positive_integer_field",
        "positive_small_integer_field",
        "small_integer_field",
        "boolean_field",
        "date_field",
        "date_time_field",
        "time_field",
        "decimal_field",
        "float_field",
    ]
