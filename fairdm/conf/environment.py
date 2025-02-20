from environ import Env

env = Env(
    # FAIRDM SETTINGS
    FAIRDM_ALLOW_DISCUSSIONS=(bool, True),
    # when False, discussion tabs are hidden from the detail views
    FAIRDM_SHOW_DATA_TABLES=(bool, True),
    # when False, data tables are hidden from the UI (useful for portals that don't make use of Sample or Measurement models)
    FAIRDM_ALLOW_PUBLIC_REGISTRATION=(bool, True),
    # when False, registrations are only allowed by invitation
    # DJANGO
    DJANGO_ADMIN_URL=(str, "admin/"),
    DJANGO_SUPERUSER_EMAIL=(str, "super.user@example.com"),
    DJANGO_ALLOW_SIGNUP=(bool, False),
    DJANGO_ALLOWED_HOSTS=(list, []),
    DJANGO_CACHE=(bool, True),
    DJANGO_DEBUG=(bool, False),
    DJANGO_READ_DOT_ENV_FILE=(bool, False),
    DJANGO_SECRET_KEY=(str, "django-insecure-qQN1YqvsY7dQ1xtdhLavAeXn1mUEAI0Wu8vkDbodEqRKkJbHyMEQS5F"),
    DJANGO_SITE_DOMAIN=(str, "localhost:8000"),
    DJANGO_SITE_ID=(int, 1),
    DJANGO_SITE_NAME=(str, "FairDM Demo"),
    DJANGO_TIME_ZONE=(str, "UTC"),
    # SECURITY
    DJANGO_SECURE_SSL_REDIRECT=(bool, True),
    DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=(bool, True),
    DJANGO_SECURE_HSTS_PRELOAD=(bool, True),
    DJANGO_SECURE_CONTENT_TYPE_NOSNIFF=(bool, True),
    DJANGO_INSECURE=(bool, False),
    # DATABASE
    POSTGRES_DB=(str, "postgres"),
    POSTGRES_PASSWORD=(str, "postgres"),
    POSTGRES_USER=(str, "postgres"),
    POSTGRES_HOST=(str, "postgres"),
    POSTGRES_PORT=(int, 5432),
    # EMAIL
    EMAIL_HOST=(str, ""),
    EMAIL_HOST_USER=(str, ""),
    EMAIL_HOST_PASSWORD=(str, ""),
    EMAIL_PORT=(int, 587),
    EMAIL_USE_TLS=(bool, True),
    EMAIL_BACKEND=(str, "django.core.mail.backends.smtp.EmailBackend"),
    # STORAGE
    S3_ENDPOINT_URL=(str, "https://media.localhost:9000"),
    S3_REGION_NAME=(str, "us-east-1"),
    S3_BUCKET_NAME=(str, "media"),
    S3_ACCESS_KEY_ID=(str, "minio"),
    S3_SECRET_ACCESS_KEY=(str, "minio123"),
    # MISCELLANEOUS
    REDIS_URL=(str, "redis://redis:6379/0"),
    USE_DOCKER=(bool, False),
    SHOW_DEBUG_TOOLBAR=(bool, False),
    LOCKDOWN_PASSWORDS=(list, []),
    LOCKDOWN_STAFF_ONLY=(bool, False),
    LOCKDOWN_SUPERUSERS_ONLY=(bool, False),
)
