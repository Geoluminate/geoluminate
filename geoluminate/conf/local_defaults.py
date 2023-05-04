from .base import *

# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")

# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 1025

# http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
INSTALLED_APPS = ["whitenoise.runserver_nostatic", *GEOLUMINATE_APPS]

# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-eager-propagates
CELERY_TASK_EAGER_PROPAGATES = True


SOCIALACCOUNT_PROVIDERS["orcid"]["BASE_DOMAIN"] = "sandbox.orcid.org"

# COMPRESS_OFFLINE = False

COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

# https://github.com/torchbox/django-libsass
# better for in-browser debugging
LIBSASS_SOURCEMAPS = True

# don't compress file during development
COMPRESS_ENABLED = False
