from geoluminate.db import models
from geoluminate.models import Measurement, Sample


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

    class Meta:
        verbose_name = "Custom Sample"
        verbose_name_plural = "Custom Samples"


class ExampleMeasurement(Measurement):
    sample = models.ForeignKey(
        "CustomSample",
        verbose_name="my custom sample",
        help_text="The sample on which the measurement was made.",
        on_delete=models.PROTECT,
    )

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
