from django.contrib.gis import admin
from polymorphic.admin import PolymorphicChildModelAdmin

from .models import Date, Description, Sample


class DescriptionInline(admin.TabularInline):
    model = Description
    fields = ["type", "text"]
    extra = 0
    max_num = 2


class DateInline(admin.TabularInline):
    model = Date
    extra = 0
    fields = ["type", "date"]


# # @admin.register(Sample)
# class SampleParentAdmin(PolymorphicParentModelAdmin):
#     base_model = Sample
#     child_models = get_subclasses(Sample, include_self=True)
#     list_display = ["id", "name", "created"]
#     exclude = ["options"]
#     list_filter = (PolymorphicChildModelFilter,)

#     def save_form(self, request: Any, form: Any, change: Any) -> Any:
#         print(form.data)
#         return super().save_form(request, form, change)


class SampleAdmin(PolymorphicChildModelAdmin):
    base_model = Sample
    inlines = [DescriptionInline, DateInline]
