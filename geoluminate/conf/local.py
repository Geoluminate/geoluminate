from split_settings.tools import include

SHOW_DEBUG_TOOLBAR = False

# imports all settings defined in the geoluminate/conf/settings/ directory
include("settings/general.py", "settings/*.py")

GEOLUMINATE_APPS = globals().get("GEOLUMINATE_APPS", [])

INSTALLED_APPS = globals().get("INSTALLED_APPS", [])

STORAGES = globals().get("STORAGES", {})

INSTALLED_APPS = (
    [
        "whitenoise.runserver_nostatic",
    ]
    + GEOLUMINATE_APPS
    + INSTALLED_APPS
    + [
        "django_extensions",
    ]
)


# http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
# INSTALLED_APPS = ["whitenoise.runserver_nostatic", *GEOLUMINATE_APPS]

# SOCIALACCOUNT_PROVIDERS["orcid"]["BASE_DOMAIN"] = "sandbox.orcid.org"

# STATICFILES OVERRIDES
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_ENABLED
COMPRESS_ENABLED = False  # don't compress during development
COMPRESS_OFFLINE = False

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
