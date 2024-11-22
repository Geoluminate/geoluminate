from geoluminate.contrib.core.tables import SampleTable

from .models import Sample


class CustomSampleTable(SampleTable):
    class Meta:
        model = Sample
        exclude = [
            "path",
            "depth",
            "status",
            "has_children",
            "has_parent",
        ]
        fields = [
            "id",
            "dataset",
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

    def render_text_field(self, value):
        return f"{value[:32]}..."

    def value_text_field(self, value):
        return value
