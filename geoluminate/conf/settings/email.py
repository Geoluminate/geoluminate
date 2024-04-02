import environ

env = environ.Env(
    DJANGO_SITE_NAME=(str, "Geoluminate Dev"),
    DJANGO_SITE_DOMAIN=(str, "localhost:8000"),
    EMAIL_HOST=(str, ""),
    EMAIL_HOST_USER=(str, ""),
    EMAIL_HOST_PASSWORD=(str, ""),
    EMAIL_PORT=(int, 587),
    EMAIL_USE_TLS=(bool, True),
    EMAIL_BACKEND=(str, "django.core.mail.backends.smtp.EmailBackend"),
)


# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = f"noreply@{env('DJANGO_SITE_DOMAIN')}"

# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = f"server@{env('DJANGO_SITE_DOMAIN')}"

# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = env("EMAIL_HOST")

# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = env("EMAIL_PORT")

# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env("EMAIL_BACKEND")

# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5
""""""

# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = f"[{env('DJANGO_SITE_NAME') or env('DJANGO_SITE_DOMAIN')}]"
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
