from django.contrib import admin

# AutoNumberInput,
# ButtonGroup,
# IconGroup,
# TagTypeFormField,
from solo.admin import SingletonModelAdmin

# from .forms import ConfigurationForm
# from .models import Configuration
from .models import Authority, Database


@admin.register(Authority)
class SiteConfigurationAdmin(SingletonModelAdmin):
    pass


admin.site.register(Database, SingletonModelAdmin)
# form = ConfigurationForm
# fieldsets = (
#     (
#         _("Brand"),
#         {"fields": (("logo", "icon"),)},
#     ),
#     (
#         _("Database"),
#         {
#             "fields": (
#                 ("db_name", "db_short_name"),
#                 "db_description",
#             ),
#         },
#     ),
#     (
#         _("Authority"),
#         {
#             "fields": (("auth_name", "auth_url"), "auth_description", "auth_contact"),
#         },
#     ),
#     (
#         _("Theme Customization"),
#         {
#             "fields": ("theme",),
#         },
#     ),
# )
