from environ import Env

env = Env(
    # DJANGO
    DJANGO_ADMIN_URL=(str, "admin/"),
    DJANGO_ALLOW_SIGNUP=(bool, True),
    DJANGO_ALLOWED_HOSTS=(list, []),
    DJANGO_CACHE=(bool, True),
    DJANGO_DEBUG=(bool, False),
    DJANGO_READ_DOT_ENV_FILE=(bool, False),
    DJANGO_SECRET_KEY=(str, "insecure-qQN1YqvsY7dQ1xtdhLavAeXn1mUEAI0Wu8vkDbodEqRKkJbHyMEQS5F"),
    DJANGO_SITE_DOMAIN=(str, "localhost:8000"),
    DJANGO_SITE_ID=(int, 1),
    DJANGO_SITE_NAME=(str, "Geoluminate Research Portal"),
    DJANGO_TIME_ZONE=(str, "UTC"),
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
    # MISCELLANEOUS
    REDIS_URL=(str, "redis://redis:6379/0"),
    DEBUG_TOOLBAR=(bool, False),
    USE_DOCKER=(bool, False),
    SHOW_DEBUG_TOOLBAR=(bool, False),
    LOCKDOWN_PASSWORDS=(list, []),
    LOCKDOWN_STAFF_ONLY=(bool, False),
    LOCKDOWN_SUPERUSERS_ONLY=(bool, False),
)
