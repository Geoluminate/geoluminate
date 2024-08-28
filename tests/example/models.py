from geoluminate.db import models
from geoluminate.metadata import Authority, Citation, Metadata
from geoluminate.models import Measurement, Sample


class CustomParentSample(Sample):
    # standard django fields
    char_field = models.CharField(
        "Character Field", max_length=200, help_text="Enter a string of up to 200 characters."
    )

    _description = Metadata(
        primary_data_fields=["char_field"],
        summary="",
        description="A rock sample is a naturally occurring solid material that is composed of one or more minerals or mineraloids and represents a fragment of a larger geological formation or rock unit. The sample is typically obtained from a specific location in order to study its physical properties, mineral composition, texture, structure, and formation processes.",
        authority=Authority(name="Geoluminate Developers", website="https://geoluminate.net", short_name="Geoluminate"),
        website="https://geoluminate.com",
        keywords=["example", "parent", "sample"],
        repo_url="",
        citation=Citation(text="Geoluminate Developers", doi=""),
        maintainer="Geoluminate Developers",
        maintainer_email="samuel.scott.jennings@gmail.com",
    )

    class Meta:
        verbose_name = "Rock Sample"
        verbose_name_plural = "Rock Samples"


class CustomSample(Sample):
    # standard django fields
    char_field = models.CharField(
        "Character Field", max_length=200, help_text="Enter a string of up to 200 characters."
    )
    text_field = models.TextField("Text Field", help_text="Enter a large amount of text.")
    integer_field = models.IntegerField("Integer Field", help_text="Enter an integer.")
    big_integer_field = models.BigIntegerField("Big Integer Field", help_text="Enter a large integer.")
    positive_integer_field = models.PositiveIntegerField(
        "Positive Integer Field", help_text="Enter a positive integer."
    )
    positive_small_integer_field = models.PositiveSmallIntegerField(
        "Positive Small Integer Field", help_text="Enter a small positive integer."
    )
    small_integer_field = models.SmallIntegerField("Small Integer Field", help_text="Enter a small integer.")
    boolean_field = models.BooleanField("Boolean Field", default=False, help_text="Select True or False.")
    date_field = models.DateField("Date Field", help_text="Select a date.")
    date_time_field = models.DateTimeField("Date Time Field", help_text="Select a date and time.")
    time_field = models.TimeField("Time Field", help_text="Select a time.")
    decimal_field = models.DecimalField(
        "Decimal Field", max_digits=5, decimal_places=2, help_text="Enter a decimal number."
    )
    float_field = models.FloatField("Float Field", help_text="Enter a floating point number.")

    _description = Metadata(
        primary_data_fields=["char_field"],
        summary="",
        description="A thin section is a small, flat slice of rock, mineral, or other material that has been carefully ground and polished to a standard thickness, typically around 30 micrometers (0.03 millimeters). This thinness allows light to pass through the sample when viewed under a polarizing light microscope. Thin sections are used in petrography (the study of rocks) and mineralogy to examine the optical properties, texture, and microstructure of the sample, which helps in identifying the minerals present, understanding the rock's formation history, and determining its geological significance.",
        authority=Authority(name="Geoluminate Developers", website="https://geoluminate.net", short_name="Geoluminate"),
        website="https://geoluminate.com",
        keywords=["example", "parent", "sample"],
        repo_url="",
        citation=Citation(text="Geoluminate Developers", doi=""),
        maintainer="Geoluminate Developers",
        maintainer_email="samuel.scott.jennings@gmail.com",
    )

    class Meta:
        verbose_name = "Thin Section"
        verbose_name_plural = "Thin Sections"


class ExampleMeasurement(Measurement):
    # standard django fields
    char_field = models.CharField(
        "Character Field", max_length=200, help_text="Enter a string of up to 200 characters."
    )
    text_field = models.TextField("Text Field", help_text="Enter a large amount of text.")
    integer_field = models.IntegerField("Integer Field", help_text="Enter an integer.")
    big_integer_field = models.BigIntegerField("Big Integer Field", help_text="Enter a large integer.")
    positive_integer_field = models.PositiveIntegerField(
        "Positive Integer Field", help_text="Enter a positive integer."
    )
    positive_small_integer_field = models.PositiveSmallIntegerField(
        "Positive Small Integer Field", help_text="Enter a small positive integer."
    )
    small_integer_field = models.SmallIntegerField("Small Integer Field", help_text="Enter a small integer.")
    boolean_field = models.BooleanField("Boolean Field", default=False, help_text="Select True or False.")
    date_field = models.DateField("Date Field", help_text="Select a date.")
    date_time_field = models.DateTimeField("Date Time Field", help_text="Select a date and time.")
    time_field = models.TimeField("Time Field", help_text="Select a time.")
    decimal_field = models.DecimalField(
        "Decimal Field", max_digits=5, decimal_places=2, help_text="Enter a decimal number."
    )
    float_field = models.FloatField("Float Field", help_text="Enter a floating point number.")

    _description = Metadata(
        primary_data_fields=["value"],
        # primary_data_types = ["float"],
        summary="Example Measurement",
        description="An example measurement model.",
        authority=Authority(name="Geoluminate Developers", website="https://geoluminate.net", short_name="Geoluminate"),
        website="https://geoluminate.com",
        keywords=["example", "measurement"],
        repo_url="",
        citation=Citation(text="Geoluminate Developers", doi=""),
        maintainer="Geoluminate Developers",
        maintainer_email="contact@geoluminate.com",
    )
