import logging
import os

from django.utils.translation import gettext_lazy as _
from split_settings.tools import include

logger = logging.getLogger(__name__)

include("settings/*.py")


def deferred_settings(config, use_celery=True):
    """This function updates settings that require information provided by the developer.

    Args:
        config (_type_): project settings

    Raises:
        ImproperlyConfigured: _description_
    """

    env = config["env"]
    basedir = config["BASE_DIR"]

    DEBUG = env.bool("DJANGO_DEBUG", False)

    GEOLUMINATE = config["GEOLUMINATE"]

    WORKDIR = GEOLUMINATE["db_acronym"].lower()

    config["APPS_DIR"] = basedir / "apps"

    PROJ_DIR = basedir / "project"

    APPS_DIR = PROJ_DIR / "apps"

    config["SITE_NAME"] = GEOLUMINATE["db_name"]

    config["META_SITE_NAME"] = GEOLUMINATE["db_name"]

    # update admin sidebar so that specified database is listed first
    config["JAZZMIN_SETTINGS"]["order_with_respect_to"].append(WORKDIR)

    # SETUP ADMIN
    # fmt: on/off
    config["JAZZMIN_SETTINGS"].update(
        dict(
            site_title=GEOLUMINATE["db_name"],
            site_header=GEOLUMINATE["db_name"],
            # welcome_sign=_(
            #     f"Welcome to the admin site for the {config['DATABASE_NAME']}. Only administrators can access this section. If you would like to become an administrator, please contact the {config['GOVERNING_BODY']}"
            # ),
            copyright=GEOLUMINATE["governing_body"]["name"],
        )
    )

    config["SPECTACULAR_SETTINGS"].update(
        {
            "TITLE": f"{GEOLUMINATE['db_name']} API",
            "DESCRIPTION": f"Documentation of API endpoints of {GEOLUMINATE['db_name']}",
        }
    )

    config["INSTALLED_APPS"] = config["GEOLUMINATE_APPS"] + config["INSTALLED_APPS"]

    config["INSTALLED_APPS"] += ["compressor"]

    # Direct Django to the following directories to search for project fixtures,
    # staticfiles and locales
    # --------------------------------------------------------------------------
    # https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
    config["FIXTURE_DIRS"] = (str(PROJ_DIR / "fixtures"),)

    # https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS

    config["STATICFILES_DIRS"] = [
        str(PROJ_DIR / "static"),
    ]

    # https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
    config["LOCALE_PATHS"] = [str(PROJ_DIR / "locale")]

    # Collect static and save media to the application base directory
    # --------------------------------------------------------------------------

    # https://docs.djangoproject.com/en/dev/ref/settings/#static-root
    config["STATIC_ROOT"] = str(basedir / "static")

    # https://docs.djangoproject.com/en/dev/ref/settings/#media-root
    config["MEDIA_ROOT"] = str(basedir / "media")

    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-broker_url

    if not use_celery:
        config["CELERY_BROKER_URL"] = env("CELERY_BROKER_URL", None)

        # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_backend
        config["CELERY_RESULT_BACKEND"] = config["CELERY_BROKER_URL"]

    config["ACCOUNT_ALLOW_REGISTRATION"] = env.bool(
        "DJANGO_ACCOUNT_ALLOW_REGISTRATION", True
    )

    # if staticfiles:
    logger.info("Applying static files configuration to Django settings.")

    # Ensure STATIC_ROOT exists.
    os.makedirs(config["STATIC_ROOT"], exist_ok=True)

    # # Insert Whitenoise Middleware.
    # config["MIDDLEWARE"] = tuple(
    #     ["whitenoise.middleware.WhiteNoiseMiddleware"] + list(config["MIDDLEWARE"])
    # )

    # # Enable GZip.
    # config[
    #     "STATICFILES_STORAGE"
    # ] = "whitenoise.storage.CompressedManifestStaticFilesStorage"

    # if os.environ.get("DJANGO_ENV") != "development":
    #     if "*" in config["ALLOWED_HOSTS"]:
    #         raise ImproperlyConfigured(
    #             '"ALLOWED_HOSTS" settings cannot contain "*" except in the development environment'
    #         )
    #     if not config["ALLOWED_HOSTS"]:
    #         raise ImproperlyConfigured('You must set a value in "ALLOWED_HOSTS"')
