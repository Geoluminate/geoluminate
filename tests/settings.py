import os
from pathlib import Path

import geoluminate

INSTALLED_APPS = [
    "example",
]

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
os.environ.setdefault("CACHE", "False")
cache = False
geoluminate.setup(development=True)

SITE_ID = 1
SITE_NAME = "Geoluminate"
SITE_DOMAIN = "localhost:8000"

SPAGHETTI_SAUCE = {
    "apps": ["filer", "user", "account", "socialaccount"],
    "show_fields": False,
}


WSGI_APPLICATION = "tests.wsgi.application"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


AWS_USE_SSL = False


WEBPACK_LOADER = {
    "GEOLUMINATE": {
        "CACHE": False,
        "STATS_FILE": BASE_DIR / "assets" / "webpack-stats.json",
        "POLL_INTERVAL": 0.1,
        "IGNORE": [r".+\.hot-update.js", r".+\.map"],
    },
}


# overwrite staticfiles storage for development
STORAGES["staticfiles"] = {
    "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
}
