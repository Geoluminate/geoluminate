from split_settings.tools import include
import geoluminate
from pathlib import Path

SHOW_DEBUG_TOOLBAR = False

# imports all settings defined in the geoluminate/conf/settings/ directory
include("settings/general.py", "settings/*.py")

INSTALLED_APPS = GEOLUMINATE_APPS + INSTALLED_APPS + ["compressor", "django_extensions"]

DEBUG = True

# http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
# INSTALLED_APPS = ["whitenoise.runserver_nostatic", *GEOLUMINATE_APPS]

# SOCIALACCOUNT_PROVIDERS["orcid"]["BASE_DOMAIN"] = "sandbox.orcid.org"

# STATICFILES OVERRIDES
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_ENABLED
COMPRESS_ENABLED = False  # don't compress during development
COMPRESS_OFFLINE = False
# STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# INSTALLED_APPS += ["django_extensions"]  # F405

LOCKDOWN_ENABLED = False



