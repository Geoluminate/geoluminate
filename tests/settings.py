"""
Django settings for example project.
"""
import os
from pathlib import Path

import environ

from geoluminate.conf.base import *
from geoluminate.conf.base import deferred_settings

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(BASE_DIR / ".env"))

# Application definition
INSTALLED_APPS = []

SPAGHETTI_SAUCE = {
    "apps": ["filer", "user", "account", "socialaccount"],
    "show_fields": False,
}

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.spatialite",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
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

INSTALLED_APPS += ["compressor"]

COMPRESS_OFFLINE = False

COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

if not os.getenv("DOCS"):
    INSTALLED_APPS += ["example"]
