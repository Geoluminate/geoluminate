"""
Django settings for example project.

"""
from pathlib import Path

import environ
from django.utils.translation import gettext_lazy as _

from geoluminate.conf.base import *  # noqa
from geoluminate.conf.base import deferred_settings

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(BASE_DIR / ".env"))

GEOLUMINATE = {
    "db_name": "Global Heat Flow Database",
    "db_acronym": "GHFDB",
    "governing_body": {
        "name": "International Heat Flow Commission",
        "short_name": "IHFC",
        "website": "https://www.ihfc-iugg.org",
    },
    "base_model": "geoluminate.contrib.gis.base.AbstractSite",
    "keywords": ["heat flow", "geothermal", "geoenergy"],
}

# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("Sam Jennings", "jennings@gfz-potsdam.de")]

# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS


# DEBUG = True

# Application definition

INSTALLED_APPS = []


SPAGHETTI_SAUCE = {
    "apps": ["filer", "user", "account", "socialaccount", "ror"],
    "show_fields": False,
}

deferred_settings(globals())

from geoluminate.conf.local_defaults import *

DEBUG = True
ROOT_URLCONF = "tests.urls"

SECRET_KEY = "g8ktwj_nj0s*h54*$rfmg19rdzi@cam5xh!wfh&g9#bvnfhcos"

WSGI_APPLICATION = "tests.wsgi.application"

LOCKDOWN_ENABLED = False

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

WHITENOISE_AUTOREFRESH = True

# WHITENOISE_USE_FINDERS = True
# print(WHITENOISE_USE_FINDERS)
INSTALLED_APPS += ["compressor"]

COMPRESS_OFFLINE = False

COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)
