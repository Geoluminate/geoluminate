from fairdm.core.models import Measurement, Sample
from fairdm.db import models


class CustomParentSample(Sample):
    char_field = models.CharField(
        "Character Field", max_length=200, help_text="Enter a string of up to 200 characters."
    )

    class FairDM:
        primary_data_fields = ["char_field"]
        description = "A rock sample is a naturally occurring solid material that is composed of one or more minerals or mineraloids and represents a fragment of a larger geological formation or rock unit. The sample is typically obtained from a specific location in order to study its physical properties, mineral composition, texture, structure, and formation processes."
        keywords = []
        filterset_fields = ["name", "char_field"]
        filterset_class = "example.filters.SampleFilter"
        # table_class = "example.tables.CustomSampleTable"
        # resource_kwargs = {"fields": ["name", "char_field"]}
        fields = ["name", "char_field", "created"]

    class Meta:
        verbose_name = "Rock Sample"
        verbose_name_plural = "Rock Samples"


class CustomSample(Sample):
    char_field = models.CharField(
        "Character Field", max_length=200, help_text="Enter a string of up to 200 characters.", blank=True, null=True
    )
    text_field = models.TextField("Text Field", help_text="Enter a large amount of text.", blank=True, null=True)
    integer_field = models.IntegerField("Integer Field", help_text="Enter an integer.", blank=True, null=True)
    big_integer_field = models.BigIntegerField(
        "Big Integer Field", help_text="Enter a large integer.", blank=True, null=True
    )
    positive_integer_field = models.PositiveIntegerField(
        "Positive Integer Field", help_text="Enter a positive integer.", blank=True, null=True
    )
    positive_small_integer_field = models.PositiveSmallIntegerField(
        "Positive Small Integer Field", help_text="Enter a small positive integer.", blank=True, null=True
    )
    small_integer_field = models.SmallIntegerField(
        "Small Integer Field", help_text="Enter a small integer.", blank=True, null=True
    )
    boolean_field = models.BooleanField(
        "Boolean Field", default=False, help_text="Select True or False.", blank=True, null=True
    )
    date_field = models.DateField("Date Field", help_text="Select a date.", blank=True, null=True)
    date_time_field = models.DateTimeField(
        "Date Time Field", help_text="Select a date and time.", blank=True, null=True
    )
    time_field = models.TimeField("Time Field", help_text="Select a time.", blank=True, null=True)
    decimal_field = models.DecimalField(
        "Decimal Field", max_digits=5, decimal_places=2, help_text="Enter a decimal number.", blank=True, null=True
    )
    float_field = models.FloatField("Float Field", help_text="Enter a floating point number.", blank=True, null=True)

    class FairDM:
        primary_data_fields = ["char_field"]
        description = "A thin section is a small, flat slice of rock, mineral, or other material that has been carefully ground and polished to a standard thickness, typically around 30 micrometers (0.03 millimeters). This thinness allows light to pass through the sample when viewed under a polarizing light microscope. Thin sections are used in petrography (the study of rocks) and mineralogy to examine the optical properties, texture, and microstructure of the sample, which helps in identifying the minerals present, understanding the rock's formation history, and determining its geological significance."
        keywords = []
        filterset_class = "example.filters.CustomSampleFilter"
        table_class = "example.tables.CustomSampleTable"

    class Meta:
        verbose_name = "Thin Section"
        verbose_name_plural = "Thin Sections"


class ExampleMeasurement(Measurement):
    # standard django fields
    char_field = models.CharField(
        "Character Field", max_length=200, help_text="Enter a string of up to 200 characters.", blank=True, null=True
    )
    text_field = models.TextField("Text Field", help_text="Enter a large amount of text.", blank=True, null=True)
    integer_field = models.IntegerField("Integer Field", help_text="Enter an integer.", blank=True, null=True)
    big_integer_field = models.BigIntegerField(
        "Big Integer Field", help_text="Enter a large integer.", blank=True, null=True
    )
    positive_integer_field = models.PositiveIntegerField(
        "Positive Integer Field", help_text="Enter a positive integer.", blank=True, null=True
    )
    positive_small_integer_field = models.PositiveSmallIntegerField(
        "Positive Small Integer Field", help_text="Enter a small positive integer.", blank=True, null=True
    )
    small_integer_field = models.SmallIntegerField(
        "Small Integer Field", help_text="Enter a small integer.", blank=True, null=True
    )
    boolean_field = models.BooleanField(
        "Boolean Field", default=False, help_text="Select True or False.", blank=True, null=True
    )
    date_field = models.DateField("Date Field", help_text="Select a date.", blank=True, null=True)
    date_time_field = models.DateTimeField(
        "Date Time Field", help_text="Select a date and time.", blank=True, null=True
    )
    time_field = models.TimeField("Time Field", help_text="Select a time.", blank=True, null=True)
    decimal_field = models.DecimalField(
        "Decimal Field", max_digits=5, decimal_places=2, help_text="Enter a decimal number.", blank=True, null=True
    )
    float_field = models.FloatField("Float Field", help_text="Enter a floating point number.", blank=True, null=True)

    class FairDM:
        description = ("An example measurement model.",)
        keywords = []

        filterset_class = "example.filters.CustomSampleFilter"
        # table_class = "example.tables.CustomSampleTable"
