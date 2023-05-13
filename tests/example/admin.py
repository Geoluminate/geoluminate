from django.contrib import admin
from example.models import TestData


@admin.register(TestData)
class TestDataAdmin(admin.ModelAdmin):
    list_display = [
        "some_field",
        "vocab_single",
        # "vocab_multi",
    ]
