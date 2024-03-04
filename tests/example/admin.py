from django.contrib import admin
from example.models import ExampleModel


@admin.register(ExampleModel)
class TestDataAdmin(admin.ModelAdmin):
    list_display = [
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
        # "quantity_field",
    ]
