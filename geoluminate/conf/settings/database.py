import environ

env = environ.Env()


# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USERNAME"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": "localhost",
        "CONN_MAX_AGE": 0,
        "ATOMIC_REQUESTS": True,
    },
}


DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"

DBBACKUP_STORAGE_OPTIONS = {"location": "/home/samjennings/backups/database/"}


DBBACKUP_FILENAME_TEMPLATE = "{databasename}-{servername}-{datetime}.{extension}"

DBBACKUP_MEDIA_FILENAME_TEMPLATE = (
    "{databasename}_media-{servername}-{datetime}.{extension}"
)

# DBBACKUP_CLEANUP_FILTER = ''

DBBACKUP_CLEANUP_KEEP = 10
