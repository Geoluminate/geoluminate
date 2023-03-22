import environ

env = environ.Env()


# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    # DATABASE_URL var is set in compose/production/django/entrypoint.sh
    {"default": env.db("DATABASE_URL")}
    # "default": {
    #     "ENGINE": "django.contrib.gis.db.backends.postgis",
    #     "NAME": env("POSTGRES_DB"),
    #     "USER": env("POSTGRES_USER"),
    #     "PASSWORD": env("POSTGRES_PASSWORD"),
    #     "HOST": "localhost",
    #     "CONN_MAX_AGE": 0,
    #     "ATOMIC_REQUESTS": True,
    # },
}

DATABASES["default"]["ATOMIC_REQUESTS"] = True


DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"

DBBACKUP_STORAGE_OPTIONS = {"location": "/home/samjennings/backups/database/"}


DBBACKUP_FILENAME_TEMPLATE = "{databasename}-{servername}-{datetime}.{extension}"

DBBACKUP_MEDIA_FILENAME_TEMPLATE = (
    "{databasename}_media-{servername}-{datetime}.{extension}"
)

# DBBACKUP_CLEANUP_FILTER = ''

DBBACKUP_CLEANUP_KEEP = 10