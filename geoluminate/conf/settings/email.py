import tldextract

BASE_DOMAIN = tldextract.extract(GEOLUMINATE["application"]["domain"]).registered_domain


# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL",
    default=f"noreply@{BASE_DOMAIN}",
    # default=f'{GEOLUMINATE["database"]["name"]} <noreply@{BASE_DOMAIN}>',
)

# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = f"server@{BASE_DOMAIN}"


# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")

# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 1025

# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)

# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5
""""""


# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = env(
    "DJANGO_EMAIL_SUBJECT_PREFIX",
    default="[Global Heat Flow Database]",
)
