DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'

DBBACKUP_STORAGE_OPTIONS = {'location': '/home/samjennings/backups/database/'}


DBBACKUP_FILENAME_TEMPLATE = '{databasename}-{servername}-{datetime}.{extension}'

DBBACKUP_MEDIA_FILENAME_TEMPLATE = '{databasename}_media-{servername}-{datetime}.{extension}'

# DBBACKUP_CLEANUP_FILTER = ''

DBBACKUP_CLEANUP_KEEP = 10