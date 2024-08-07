from django.contrib import admin
from example.models import CustomParentSample, CustomSample, ExampleMeasurement

# from geoluminate.admin import SampleAdmin

admin.site.register(CustomParentSample, admin.ModelAdmin)


@admin.register(ExampleMeasurement)
class TestDataAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomSample)
class CustomSampleAdmin(admin.ModelAdmin):
    pass
