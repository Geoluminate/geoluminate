import os


env = globals()["env"]


DEBUG = env.bool("DJANGO_DEBUG")

ACCOUNT_EMAIL_VERIFICATION = "optional"
ALLOWED_HOSTS = ["*"]
AUTH_PASSWORD_VALIDATORS = []
AWS_USE_SSL = False

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
SECURE_SSL_REDIRECT = False
DATABASES = {
    "default": {
        "ATOMIC_REQUESTS": True,
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "CONN_MAX_AGE": 60,
    }
}


STORAGES["default"] = {
    "BACKEND": "django.core.files.storage.FileSystemStorage",
}

THUMBNAIL_DEFAULT_STORAGE = "easy_thumbnails.storage.ThumbnailFileSystemStorage"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        "LOCATION": "",
    },
    "select2": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    },
}


CACHES["vocabularies"] = {
    "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
    "LOCATION": BASE_DIR / ".vocabularies-cache",
}

VOCABULARY_DEFAULT_CACHE = "vocabularies"


SHELL_PLUS = "ipython"

# STATIC FILES OVERRIDES
INSTALLED_APPS.insert(0, "whitenoise.runserver_nostatic")
COMPRESS_OFFLINE = False
COMPRESS_ENABLED = False

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


INTERNAL_IPS = ["127.0.0.1"]

CORS_ALLOW_ALL_ORIGINS = True

AWS_S3_URL_PROTOCOL = "http:"
