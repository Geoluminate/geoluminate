import tldextract
import environ



BASE_DOMAIN = tldextract.extract(GEOLUMINATE["application"]["domain"]).registered_domain


env = environ.Env(
    DEFAULT_FROM_EMAIL=(str, f"noreply@{BASE_DOMAIN}"),
    SERVER_EMAIL=(str, f"server@{BASE_DOMAIN}"),
    EMAIL_HOST=(str, ""),
    EMAIL_HOST_USER=(str, ""),
    EMAIL_HOST_PASSWORD=(str, ""),
    EMAIL_PORT=(int, 587),
    EMAIL_USE_TLS=(bool, True),
    EMAIL_BACKEND=(str, "django.core.mail.backends.smtp.EmailBackend"),
)


# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")

# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = env("SERVER_EMAIL")

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
EMAIL_SUBJECT_PREFIX = f"[{BASE_DOMAIN}]"
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
EMAIL_BACKEND = env("EMAIL_BACKEND")
