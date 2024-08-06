from django.contrib import admin
from example.models import CustomSample, ExampleMeasurement

from geoluminate.admin import MeasurementAdmin, SampleAdmin


@admin.register(ExampleMeasurement)
class TestDataAdmin(MeasurementAdmin):
    pass


@admin.register(CustomSample)
class CustomSampleAdmin(SampleAdmin):
    pass
