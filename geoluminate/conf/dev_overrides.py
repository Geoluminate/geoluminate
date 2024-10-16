import os

env = globals()["env"]

DEBUG = env.bool("DJANGO_DEBUG")

ALLOWED_HOSTS = ["*"]
AUTH_PASSWORD_VALIDATORS = []
ACCOUNT_EMAIL_VERIFICATION = "optional"
COMPRESS_OFFLINE = False
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
AWS_USE_SSL = False
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


STORAGES["default"] = {
    "BACKEND": "django.core.files.storage.FileSystemStorage",
}

THUMBNAIL_DEFAULT_STORAGE = "easy_thumbnails.storage.ThumbnailFileSystemStorage"

CACHES["vocabularies"] = {
    "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
    "LOCATION": BASE_DIR / ".vocabularies-cache",
}

VOCABULARY_DEFAULT_CACHE = "vocabularies"


SHELL_PLUS = "ipython"

INSTALLED_APPS.insert(0, "whitenoise.runserver_nostatic")


if env("USE_DOCKER"):
    WEBPACK_LOADER = {
        "GEOLUMINATE": {
            "CACHE": False,
            "STATS_FILE": BASE_DIR / "assets" / "webpack-stats.json",
            "POLL_INTERVAL": 0.1,
            "IGNORE": [r".+\.hot-update.js", r".+\.map"],
        },
    }

if env("SHOW_DEBUG_TOOLBAR"):
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

# if env("DJANGO_CACHE"):


INTERNAL_IPS = ["127.0.0.1"]

ROOT_URLCONF = "geoluminate.urls"

AWS_S3_URL_PROTOCOL = "http:"
