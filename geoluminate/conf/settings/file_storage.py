import os

# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = COMPRESS_ROOT = str(BASE_DIR / "staticfiles")

# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_URL
STATIC_URL = COMPRESS_URL = "/static/"


# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(BASE_DIR / "media")

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS

STATICFILES_DIRS = [
    # str(BASE_DIR / "project" / "static"),
    # str(BASE_DIR / "assets"),
    # str(BASE_DIR / "static"),
    # ("node_modules", BASE_DIR / "node_modules"),
]

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]


# django-compressor
# ------------------------------------------------------------------------------
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_ENABLED
COMPRESS_ENABLED = True

# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_STORAGE
COMPRESS_STORAGE = "compressor.storage.GzipCompressorFileStorage"

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

AWS_S3_ENDPOINT_URL = "http://storage:9000"


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


STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "location": "public",
            "bucket_name": "geoluminate",
            "default_acl": "public-read",
            # "file_overwrite": False,
            "url_protocol": "http:",
        },
    },
    "private": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "location": "private",
            "bucket_name": "geoluminate",
            "url_protocol": "http:",
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
        "OPTIONS": {
            "location": "static",
            "bucket_name": "geoluminate",
            "default_acl": "public-read",
            "url_protocol": "http:",
        },
    },
}

# main = STORAGES["default"]
# main.update
FILER_STORAGES = {
    "public": {
        "main": {
            "ENGINE": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "location": "public/filer/original/",
                "url_protocol": "http:",
            },
            "UPLOAD_TO": "filer.utils.generate_filename.randomized",
            "UPLOAD_TO_PREFIX": "filer_public",
        },
        "thumbnails": {
            "ENGINE": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "location": "public/filer/thumbs/",
                "url_protocol": "http:",
                # "base_url": "filer_thumbnails",
            },
        },
    },
    "private": {
        "main": {
            "ENGINE": "filer.storage.PrivateFileSystemStorage",
            "OPTIONS": {
                "location": "/path/to/smedia/filer",
                "base_url": "/smedia/filer/",
            },
            "UPLOAD_TO": "filer.utils.generate_filename.randomized",
            "UPLOAD_TO_PREFIX": "filer_public",
        },
        "thumbnails": {
            "ENGINE": "filer.storage.PrivateFileSystemStorage",
            "OPTIONS": {
                "location": "/path/to/smedia/filer_thumbnails",
                "base_url": "/smedia/filer_thumbnails/",
            },
        },
    },
}


FILER_FILE_STORAGE_BACKEND = STORAGES["default"]

THUMBNAIL_DEFAULT_STORAGE = STORAGES["default"]