import os
import socket
import sys
from contextlib import suppress
from template_partials.apps import wrap_loaders

from django.contrib.messages import constants as messages
from django.core.exceptions import ImproperlyConfigured

env = globals()["env"]

GIS_ENABLED = False

with suppress(ImproperlyConfigured):
    import django.contrib.gis.db.models  # noqa

    GIS_ENABLED = True


# sys.path.append(os.path.join(BASE_DIR, "project", "schemas"))

GEOLUMINATE = globals().get("GEOLUMINATE", {})

ADMIN_URL = f"{env('DJANGO_ADMIN_URL')}"
ADMINS = [("Super User", env("DJANGO_SUPERUSER_EMAIL"))]
# ADMINS = [(admin["name"], admin["email"]) for admin in GEOLUMINATE["application"]["developers"]]
ALLOWED_HOSTS = [env("DJANGO_SITE_DOMAIN")] + env("DJANGO_ALLOWED_HOSTS")
MANAGERS = ADMINS
ROOT_URLCONF = "config.urls"
SECRET_KEY = env("DJANGO_SECRET_KEY")
SITE_DOMAIN = env("DJANGO_SITE_DOMAIN")
SITE_ID = env("DJANGO_SITE_ID")
SITE_NAME = META_SITE_NAME = env("DJANGO_SITE_NAME")
TIME_ZONE = env("DJANGO_TIME_ZONE", default="UTC")
USE_TZ = True
WSGI_APPLICATION = None

# Coloured Messages
MESSAGE_TAGS = {
    messages.DEBUG: "debug alert-secondary",
    messages.INFO: "info alert-info",
    messages.SUCCESS: "success alert-success",
    messages.WARNING: "warning alert-warning",
    messages.ERROR: "error alert-danger",
}


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "OPTIONS": {
            "builtins": ["easy_icons.templatetags.easy_icons"],
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.template.context_processors.csrf",
                "django.template.context_processors.tz",
                "sekizai.context_processors.sekizai",
                "django.template.context_processors.static",
                "geoluminate.core.utils.context_processor",
            ],
        },
    },
]
# for django-template-partials to work alongside django-admin-tools (for some reason, wrap_loaders is not working)
default_loaders = [
    "admin_tools.template_loaders.Loader",
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]
cached_loaders = [("django.template.loaders.cached.Loader", default_loaders)]
partial_loaders = [("template_partials.loader.Loader", cached_loaders)]

TEMPLATES[0]["OPTIONS"]["loaders"] = partial_loaders


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "lockdown.middleware.LockdownMiddleware",
]

# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"


# for django debug toolbar
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]


# Direct Django to the following directories to search for project fixtures,
# staticfiles and locales
# --------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(BASE_DIR / "project" / "fixtures"),)


# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [str(BASE_DIR / "project" / "locale")]


# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap5-responsive.html"

ACCOUNT_MANAGEMENT_GET_AVATAR_URL = "geoluminate.contrib.contributors.utils.get_contributor_avatar"  # This line connects the avatar_url template tag to the function that retrieves the contributor's avatar URL.  # noqa: E501

# DEPLOYMENT_PIPELINE = {}
DJANGO_SETUP_TOOLS = {
    # "default": {},
    "": {
        "on_initial": [
            ("makemigrations", "--no-input"),
            ("migrate", "--no-input"),
            ("createsuperuser", "--no-input"),
            ("loaddata", "creativecommons"),
        ],
        "always_run": [
            ("migrate", "--no-input"),
            ("collectstatic", "--noinput"),
            ("compress",),
            "django_setup_tools.scripts.sync_site_id",
        ],
    },
    "development": {
        "merge": True,  # merge with the default commands
        "on_initial": [
            ("loaddata", "myapp"),
        ],
        "always_run": [
            "django_setup_tools.scripts.some_extra_func",
        ],
    },
}
