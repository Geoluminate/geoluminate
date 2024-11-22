from geoluminate.contrib.core.filters import SampleFilter

from .models import CustomSample


class CustomSampleFilter(SampleFilter):
    class Meta:
        model = CustomSample
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
