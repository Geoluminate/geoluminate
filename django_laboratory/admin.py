from django.contrib import admin
from .models import Laboratory, Manufacturer, Instrument


@admin.register(Laboratory)
class LaboratoryAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = [
        'instrument_id',
        'type',
        'model',
        'laboratory',
        'manufacturer',
        'year_manufactured']
    list_filter = ['manufacturer', 'model']

    search_fields = ['laboratory__name', 'model', 'type', 'instrument_id']
