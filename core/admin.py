from django.contrib import admin
from django.contrib.admin.models import LogEntry
from solo.admin import SingletonModelAdmin
from core.models import SiteConfiguration

# @admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    # to have a date-based drilldown navigation in the admin page
    date_hierarchy = 'action_time'

    # to filter the resultes by users, content types and action flags
    list_filter = [
        'user',
        'content_type',
        'action_flag',
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'change_message',
        'action_flag',
    ]


admin.site.register(SiteConfiguration, SingletonModelAdmin)