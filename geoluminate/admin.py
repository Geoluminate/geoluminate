from actstream.models import Action, Follow
from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from geoluminate.contrib.measurements.admin import MeasurementAdmin
from geoluminate.contrib.samples.admin import SampleAdmin

admin.site.site_header = settings.SITE_NAME + _("Admin")

admin.site.unregister(Action)
admin.site.unregister(Follow)


__all__ = ["MeasurementAdmin", "SampleAdmin"]
