import os

# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# https://docs.djangoproject.com/en/dev/ref/settings/#databases


if os.getenv("DATABASE_URL"):
    DATABASES = {"default": env.db("DATABASE_URL")}

    DATABASES["default"]["ATOMIC_REQUESTS"] = True
    DATABASES["default"]["ENGINE"] = "django.contrib.gis.db.backends.postgis"
    DATABASES["default"]["CONN_MAX_AGE"] = env.int(
        "CONN_MAX_AGE", default=60
    )  # noqa F405

DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"

DBBACKUP_STORAGE_OPTIONS = {"location": "/home/samjennings/backups/database/"}


DBBACKUP_FILENAME_TEMPLATE = "{databasename}-{servername}-{datetime}.{extension}"

DBBACKUP_MEDIA_FILENAME_TEMPLATE = (
    "{databasename}_media-{servername}-{datetime}.{extension}"
)

# DBBACKUP_CLEANUP_FILTER = ''

DBBACKUP_CLEANUP_KEEP = 10

