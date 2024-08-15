DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# DATABASES = {"default": env.db()}
# DATABASES["default"]["ATOMIC_REQUESTS"] = True
# DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)  # noqa F405

DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"

DBBACKUP_STORAGE_OPTIONS = {"location": "/app/dbbackups/"}


DBBACKUP_FILENAME_TEMPLATE = "{databasename}-{servername}-{datetime}.{extension}"

DBBACKUP_MEDIA_FILENAME_TEMPLATE = "{databasename}_media-{servername}-{datetime}.{extension}"

# DBBACKUP_CLEANUP_FILTER = ''

DBBACKUP_CLEANUP_KEEP = 10
