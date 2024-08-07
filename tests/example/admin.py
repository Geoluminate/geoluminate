from django.contrib import admin
from example.models import CustomSample, ExampleMeasurement

# from geoluminate.admin import SampleAdmin


@admin.register(ExampleMeasurement)
class TestDataAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomSample)
class CustomSampleAdmin(admin.ModelAdmin):
    pass
