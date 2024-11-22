import re
from django.utils.log import RequireDebugTrue

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
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        # "BACKEND": "django.core.cache.backends.dummy.DummyCache",
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

# https://github.com/torchbox/django-libsass
LIBSASS_SOURCEMAPS = True

DEBUG_TOOLBAR_CONFIG = {
    # "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
    "ROOT_TAG_EXTRA_ATTRS": "hx-preserve",
}


class IgnoreStaticAndMediaFilter:
    def filter(self, record):
        # Access the message in record and check if it's a static or media request
        message = record.getMessage()
        return not re.match(r'^"GET /(static|media)/', message) and not re.match(r'^"GET /__debug__/', message)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {
            "()": RequireDebugTrue,  # Only log in DEBUG mode
        },
        "ignore_static_and_media": {
            "()": IgnoreStaticAndMediaFilter,
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true", "ignore_static_and_media"],
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django.server": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
