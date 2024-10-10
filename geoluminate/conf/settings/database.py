from environ import Env

env = Env(
    POSTGRES_USER=(str, "postgres"),
    POSTGRES_HOST=(str, "postgres"),
    POSTGRES_PORT=(int, 5432),
)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("POSTGRES_DB"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "USER": env.str("POSTGRES_USER"),
        "HOST": env.str("POSTGRES_HOST"),
        "PORT": env.str("POSTGRES_PORT"),
    }
}


DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)  # noqa F405

DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"
DBBACKUP_STORAGE_OPTIONS = {"location": "/app/dbbackups/"}


DBBACKUP_FILENAME_TEMPLATE = "{databasename}-{servername}-{datetime}.{extension}"

DBBACKUP_MEDIA_FILENAME_TEMPLATE = "{databasename}_media-{servername}-{datetime}.{extension}"

# DBBACKUP_CLEANUP_FILTER = ''

DBBACKUP_CLEANUP_KEEP = 10
