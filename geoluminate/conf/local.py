from split_settings.tools import include

# imports all settings defined in the geoluminate/conf/settings/ directory
include("settings/general.py", "settings/*.py")

INSTALLED_APPS = GEOLUMINATE_APPS + INSTALLED_APPS + ["compressor"]

DEBUG = True

# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_ENABLED
COMPRESS_ENABLED = False  # don't compress during development

# http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
# INSTALLED_APPS = ["whitenoise.runserver_nostatic", *GEOLUMINATE_APPS]

# SOCIALACCOUNT_PROVIDERS["orcid"]["BASE_DOMAIN"] = "sandbox.orcid.org"

COMPRESS_OFFLINE = False

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-eager-propagates
CELERY_TASK_EAGER_PROPAGATES = True

# INSTALLED_APPS += ["django_extensions"]  # F405

LOCKDOWN_ENABLED = False

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# BASE_SERIALIZER = "geoluminate.contrib.api.serializers.HyperlinkedModelSerializer"
