import socket
from contextlib import suppress

from django.contrib.messages import constants as messages
from django.core.exceptions import ImproperlyConfigured

env = globals()["env"]

GIS_ENABLED = False

with suppress(ImproperlyConfigured):
    import django.contrib.gis.db.models  # noqa

    GIS_ENABLED = True


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
            "builtins": [
                "django.templatetags.i18n",
                "django_cotton.templatetags.cotton",
                "easy_icons.templatetags.easy_icons",
            ],
        },
    },
]
# for django-template-partials to work alongside django-admin-tools (for some reason, wrap_loaders is not working)
default_loaders = [
    "admin_tools.template_loaders.Loader",
    "django_cotton.cotton_loader.Loader",
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


# DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap5-responsive.html"
DJANGO_TABLES2_TEMPLATE = "geoluminate/base/table.html"

ACCOUNT_MANAGEMENT_GET_AVATAR_URL = "geoluminate.contrib.contributors.utils.get_contributor_avatar"  # This line connects the avatar_url template tag to the function that retrieves the contributor's avatar URL.  # noqa: E501

# DEPLOYMENT_PIPELINE = {}
DJANGO_SETUP_TOOLS = {
    # "default": {},
    "": {
        "on_initial": [
            ("makemigrations", "--no-input"),
            ("migrate", "--no-input"),
            (
                "createsuperuser",
                "--no-input",
                "--first_name",
                env("DJANGO_SUPERUSER_FIRSTNAME", default="Super"),
                "--last_name",
                env("DJANGO_SUPERUSER_LASTNAME", default="User"),
            ),
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

COTTON_DIR = "components"


EASY_ICONS = {
    # the function that will be used to get the icon based on user settings
    "default_renderer": "provider",
    # default attributes applied to all icons
    "attrs": {
        # "height": "1em",
        # "fill": "currentColor",
    },
    # maps aliases to icon names
    "aliases": {
        "administration": "fas fa-toolbox",
        "activity": "activity.svg",
        "angle-left": "fas fa-angle-left",
        "angle-right": "fas fa-angle-right",
        "angles-left": "fas fa-angle-double-left",
        "angles-right": "fas fa-angle-double-right",
        "api": "fas fa-code",
        "arrow-left": "fas fa-arrow-left",
        "arrow-right": "fas fa-arrow-right",
        "arrow-up": "fas fa-arrow-up",
        "arrow-down": "fas fa-arrow-down",
        "back": "fas fa-arrow-left",
        "cancel": "fas fa-times",
        "chart": "fas fa-chart-bar",
        "close": "fas fa-times",
        "circle-half": "fas fa-circle-half-stroke",
        "comments": "fas fa-comments",
        "community": "fas fa-users",
        "contributors": "fas fa-user-friends",
        "dataset": "fas fa-folder",
        "delete": "fas fa-trash",
        "download": "fas fa-download",
        "download-zip": "fas fa-file-zipper",
        "download-xml": "filetype-xml.svg",
        "edit": "fas fa-edit",
        "email": "fas fa-envelope",
        "expand": "fas fa-expand",
        "ellipsis": "fas fa-ellipsis-v",
        # "facebook": "facebook.svg",
        "filter": "fas fa-filter",
        "globe": "fas fa-globe",
        "grid": "grid.svg",
        "home": "fas fa-home",
        "identifier": "fas fa-fingerprint",
        "image": "fas fa-image",
        "images": "fas fa-images",
        "info": "fas fa-info-circle",
        "invite": "fas fa-envelope",
        "linkedin": "fab fa-linkedin",
        "literature": "fas fa-book",
        "login": "fas fa-sign-in-alt",
        "logout": "fas fa-sign-out-alt",
        "map": "fas fa-map-marked-alt",
        "measurement": "fas fa-ruler",
        "measurements": "fas fa-ruler-combined",
        "menu": "fas fa-bars",
        "moon": "fas fa-moon",
        "orcid": "fab fa-orcid",
        "organisation": "fas fa-building",
        "organization": "fas fa-building",
        "overview": "fas fa-book-open",
        "plus": "fas fa-plus",
        "preferences": "fas fa-sliders",
        "project": "fas fa-layer-group",
        "ror": "ror.svg",
        "rotate": "fas fa-sync-alt",
        "sample": "fas fa-database",
        "search": "fas fa-search",
        "share": "fas fa-share",
        "spinner": "spinner.svg",
        "star-outline": "far fa-star",
        "star-solid": "fas fa-star",
        "sun": "fas fa-sun",
        "table": "fas fa-table",
        "upload": "fas fa-upload",
        "user-circle": "fas fa-user-circle",
        "user": "fas fa-user",
        "vocabularies": "fas fa-book-open",
        "whatsapp": "fab fa-whatsapp",
        "x_twitter": "fab fa-twitter",
        # django-account-management
        "password_change": "fas fa-key",
        "mfa": "fas fa-lock",
        "link": "fas fa-link",
        "gear": "fas fa-cog",
        "sessions": "fas fa-user-clock",
        "site_admin": "fas fa-user-cog",
    },
}
