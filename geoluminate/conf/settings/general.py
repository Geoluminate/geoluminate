import os
import socket
import sys

import environ
from django.contrib.messages import constants as messages

sys.path.append(os.path.join(BASE_DIR, "project", "schemas"))

GEOLUMINATE = globals().get("GEOLUMINATE", {})


env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    DJANGO_SECRET_KEY=(str, "HoVcnlU2IqQN1YqvsY7dQ1xtdhLavAeXn1mUEAI0Wu8vkDbodEqRKkJbHyMEQS5F"),
    # SHOW_DEBUG_TOOLBAR=(bool, False),
    DJANGO_ADMIN_URL=(str, "admin/"),
    DJANGO_ALLOWED_HOSTS=(list, []),
    DJANGO_READ_DOT_ENV_FILE=(bool, False),
    DJANGO_TIME_ZONE=(str, "UTC"),
    DJANGO_SITE_ID=(int, 1),
    DJANGO_SITE_DOMAIN=(str, "localhost:8000"),
    DJANGO_SITE_NAME=(str, "Geoluminate Research Portal"),
)

if env("DJANGO_READ_DOT_ENV_FILE"):
    # OS environment variables take precedence over variables from .env
    env.read_env(str(BASE_DIR / ".env"))


# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY")

TIME_ZONE = env("DJANGO_TIME_ZONE", default="UTC")
""""""

# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = env("DJANGO_SITE_ID")
SITE_DOMAIN = env("DJANGO_SITE_DOMAIN")
SITE_NAME = META_SITE_NAME = env("DJANGO_SITE_NAME")

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [SITE_DOMAIN] + env("DJANGO_ALLOWED_HOSTS")

# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [(admin["name"], admin["email"]) for admin in GEOLUMINATE["application"]["developers"]]
MANAGERS = ADMINS

# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "geoluminate.urls"

ADMIN_URL = f"admin-{env('DJANGO_ADMIN_URL')}"

# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = None

# Coloured Messages
MESSAGE_TAGS = {
    messages.DEBUG: "debug alert-secondary",
    messages.INFO: "info alert-info",
    messages.SUCCESS: "success alert-success",
    messages.WARNING: "warning alert-warning",
    messages.ERROR: "error alert-danger",
}

# TAGGIT_CASE_INSENSITIVE = True

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
                "geoluminate.utils.context_processor",
                # "cms.context_processors.cms_settings",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        },
    },
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    # "cms.middleware.utils.ApphookReloadMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "cms.middleware.user.CurrentUserMiddleware",
    # "cms.middleware.page.CurrentPageMiddleware",
    # "cms.middleware.toolbar.ToolbarMiddleware",
    # "cms.middleware.language.LanguageCookieMiddleware",
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


if SHOW_DEBUG_TOOLBAR:
    # GEOLUMINATE_APPS.append("debug_toolbar")
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

    DEBUG_TOOLBAR_CONFIG = {
        "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
        "SHOW_TEMPLATE_CONTEXT": True,
    }

    # DEBUG_TOOLBAR_PANELS += [
    #     "template_profiler_panel.panels.template.TemplateProfilerPanel",
    # ]

# FORM_RENDERER = "geoluminate.utils.forms.DefaultFormRenderer"

# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
