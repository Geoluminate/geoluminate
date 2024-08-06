import os

# from sentry_sdk.integrations.celery import CeleryIntegration
# from sentry_sdk.integrations.django import DjangoIntegration
# from sentry_sdk.integrations.redis import RedisIntegration


# SENTRY_INTEGRATIONS = [
#     DjangoIntegration(),
#     CeleryIntegration(),
#     RedisIntegration(),
# ]

# SENTRY_DSN = env("SENTRY_DSN")
# SENTRY_LOG_LEVEL = env.int("DJANGO_SENTRY_LOG_LEVEL", logging.INFO)

# sentry_logging = LoggingIntegration(
#     level=SENTRY_LOG_LEVEL,  # Capture info and above as breadcrumbs
#     event_level=logging.ERROR,  # Send errors as events
# )

# sentry_sdk.init(
#     dsn=SENTRY_DSN,
#     integrations=sentry_logging + SENTRY_INTEGRATIONS,
#     environment=env("SENTRY_ENVIRONMENT", default="production"),
#     traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE", default=0.0),
# )


# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {"verbose": {"format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"}},
#     "handlers": {
#         "console": {
#             "level": "DEBUG",
#             "class": "logging.StreamHandler",
#             "formatter": "verbose",
#         }
#     },
#     "root": {"level": "INFO", "handlers": ["console"]},
# }

# Logging Configuration ========================================================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            # "format": "{levelname} {asctime} {module}:{funcName} {message}",
            "format": "{levelname} {asctime} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",  # Adjust the level as needed
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        # "file": {
        #     "level": "INFO",  # Adjust the level as needed
        #     "class": "logging.FileHandler",
        #     "filename": os.path.join(BASE_DIR, "logs", "debug.log"),
        #     "formatter": "verbose",
        # },
        # "mail_admins": {"level": "ERROR", "class": "django.utils.log.AdminEmailHandler", "formatter": "simple"},
    },
    "loggers": {
        # "django": {
        #     # "handlers": ["console", "file"],
        #     "handlers": ["console"],
        #     "level": "INFO",  # Adjust the level as needed
        #     "propagate": True,
        # },
        "geoluminate": {  # Replace with the name of your Django app
            "handlers": ["console"],
            "level": "DEBUG",  # Adjust the level as needed
            "propagate": False,
        },
        # "django.request": {
        #     "handlers": ["mail_admins"],
        #     "level": "ERROR",
        #     "propagate": True,
        # },
    },
    "django_migration_zero": {
        "handlers": ["console"],
        "level": "INFO",
        "propagate": True,
    },
}
