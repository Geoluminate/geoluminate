import environ


env = environ.Env(
    USE_DOCKER=(bool, False),
    DEBUG_TOOLBAR=(bool, False),
)


ALLOWED_HOSTS = ["*"]
AUTH_PASSWORD_VALIDATORS = []
ACCOUNT_EMAIL_VERIFICATION = "optional"
COMPRESS_ENABLED = True
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

if env("DEBUG_TOOLBAR"):
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")


INTERNAL_IPS = [
    "127.0.0.1",
]
