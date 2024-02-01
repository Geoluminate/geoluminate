"""
Django settings for example project.
"""

import os
import sys
from pathlib import Path

import geoluminate

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
os.environ.setdefault("DATABASE_URL", "")
os.environ.setdefault("CACHE", "False")

# Application definition
INSTALLED_APPS = ["example"]
geoluminate.setup(development=True)

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

STATICFILES_DIRS = [
    ("node_modules", BASE_DIR / "node_modules"),
]

ROOT_URLCONF = "tests.urls"

WSGI_APPLICATION = "tests.wsgi.application"

MODELTRANSLATION_DEFAULT_LANGUAGE = "en"
