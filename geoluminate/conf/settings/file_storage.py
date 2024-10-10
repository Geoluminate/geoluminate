import os
from pathlib import Path

env = globals()["env"]


# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = COMPRESS_ROOT = str(BASE_DIR / "static")

# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = COMPRESS_URL = "/static/"


# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(BASE_DIR / "media")

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS

if os.path.exists(str(BASE_DIR / "assets")):
    STATICFILES_DIRS = [
        # this is where the end user will store their static files
        str(BASE_DIR / "assets"),
    ]

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]


# https://github.com/torchbox/django-libsass
# better for in-browser debugging
LIBSASS_SOURCEMAPS = True


# WHITENOISE
# ------------------------------------------------------------------------------

WHITENOISE_MANIFEST_STRICT = False


AWS_ACCESS_KEY_ID = os.environ.get("MINIO_ACCESS_KEY_ID")
""""""
AWS_SECRET_ACCESS_KEY = os.environ.get("MINIO_SECRET_ACCESS_KEY")
""""""
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_BUCKET_NAME")
""""""


AWS_S3_CUSTOM_DOMAIN = os.environ.get("AWS_S3_CUSTOM_DOMAIN")

AWS_S3_ENDPOINT_URL = "http://minio:9000/"

# if domain := os.environ.get("AWS_CUSTOM_DOMAIN", None):
#     AWS_S3_CUSTOM_DOMAIN = f"{domain}/{AWS_STORAGE_BUCKET_NAME}"
# else:
#     AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
#     """"""

AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
""""""

AWS_S3_REGION_NAME = os.environ.get("REGION_NAME")
""""""


AWS_DEFAULT_ACL = None
""""""

AWS_S3_URL_PROTOCOL = "https:"


# django-compressor
# ------------------------------------------------------------------------------
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_ENABLED
COMPRESS_ENABLED = True

# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_STORAGE
COMPRESS_STORAGE = "compressor.storage.GzipCompressorFileStorage"
# COMPRESS_STORAGE = "compressor.storage.CompressorFileStorage"

# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_OFFLINE
COMPRESS_OFFLINE = True  # Offline compression is required when using Whitenoise

# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_FILTERS
COMPRESS_FILTERS = {
    "css": [
        "compressor.filters.css_default.CssAbsoluteFilter",
        "compressor.filters.cssmin.rCSSMinFilter",
    ],
    "js": ["compressor.filters.jsmin.JSMinFilter"],
}

# STATIC
# ------------------------
COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "location": "public",
            "default_acl": "public-read",
            # "url_protocol": "http:" if DEBUG else "https:",
        },
    },
    "private": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "location": "private",
            "default_acl": "private",
            # "url_protocol": "http:" if DEBUG else "https:",
        },
    },
    "staticfiles": {
        # using whitenosie.storage.CompressedManifestStaticFilesStorage is more problematic than it's worth
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}


# THUMBNAIL_DEFAULT_STORAGE = STORAGES["default"]


WEBPACK_LOADER = {
    "GEOLUMINATE": {
        "CACHE": env("DJANGO_CACHE"),
        "STATS_FILE": Path(__file__).parent / "webpack-stats.prod.json",
    },
}
