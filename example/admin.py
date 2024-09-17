from django.contrib import admin

from geoluminate.contrib.samples.admin import SampleAdmin

from .models import CustomSample, ExampleMeasurement

# admin.site.register(CustomParentSample, admin.ModelAdmin)


@admin.register(ExampleMeasurement)
class TestDataAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomSample)
class CustomSampleAdmin(SampleAdmin):
    pass
