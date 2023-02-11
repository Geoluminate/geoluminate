import logging
import os

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


def geoluminate_setup(config, staticfiles=True, allowed_hosts=True, logging=True):

    if staticfiles:
        logger.info("Applying static files configuration to Django settings.")

        # Ensure STATIC_ROOT exists.
        os.makedirs(config["STATIC_ROOT"], exist_ok=True)

        # Insert Whitenoise Middleware.
        try:
            config["MIDDLEWARE_CLASSES"] = tuple(
                ["whitenoise.middleware.WhiteNoiseMiddleware"]
                + list(config["MIDDLEWARE_CLASSES"])
            )
        except KeyError:
            config["MIDDLEWARE"] = tuple(
                ["whitenoise.middleware.WhiteNoiseMiddleware"]
                + list(config["MIDDLEWARE"])
            )

        # Enable GZip.
        config[
            "STATICFILES_STORAGE"
        ] = "whitenoise.storage.CompressedManifestStaticFilesStorage"

    if allowed_hosts:
        if os.environ.get("DJANGO_ENV") != "development":
            if "*" in config["ALLOWED_HOSTS"]:
                raise ImproperlyConfigured(
                    '"ALLOWED_HOSTS" settings cannot contain "*" except in the development environment'
                )
            if not config["ALLOWED_HOSTS"]:
                raise ImproperlyConfigured('You must set a value in "ALLOWED_HOSTS"')

    if logging:
        logger.info("Applying Geoluminate logging configuration to Django settings.")

        config["LOGGING"] = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "verbose": {
                    "format": (
                        "%(asctime)s [%(process)d] [%(levelname)s] "
                        + "pathname=%(pathname)s lineno=%(lineno)s "
                        + "funcname=%(funcName)s %(message)s"
                    ),
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
                "simple": {"format": "%(levelname)s %(message)s"},
            },
            "handlers": {
                "null": {
                    "level": "DEBUG",
                    "class": "logging.NullHandler",
                },
                "console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "verbose",
                },
            },
            "loggers": {
                "testlogger": {
                    "handlers": ["console"],
                    "level": "INFO",
                }
            },
        }

    if config.get("SITE_NAME"):
        config["META_SITE_NAME"] = config["SITE_NAME"]
    else:
        config["META_SITE_NAME"] = config["SITE_NAME"] = config["DATABASE_NAME"]

    # SETUP ADMIN
    # fmt: on/off
    config["JAZZMIN_SETTINGS"].update(
        dict(
            site_title=config["DATABASE_NAME"],
            site_header=config["DATABASE_NAME"],
            welcome_sign=_(
                f"Welcome to the admin site for the {config['DATABASE_NAME']}. Only administrators can access this section. If you would like to become an administrator, please contact the {config['GOVERNING_BODY']}"
            ),
            copyright=config["GOVERNING_BODY"],
        )
    )
