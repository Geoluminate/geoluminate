from configuration.models import Configuration
from django.contrib import admin

from geoluminate.contrib.measurements.admin import MeasurementAdmin
from geoluminate.contrib.samples.admin import SampleAdmin

config = Configuration.get_solo()

# will probably need to work out a way to refresh these when changes are made to the config object
admin.site.site_header = config.database["name"]
admin.site.site_title = config.database["name"]

__all__ = ["MeasurementAdmin", "SampleAdmin"]
