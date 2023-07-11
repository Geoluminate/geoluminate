import os
import socket
import sys

import environ
import yaml
from django.contrib.messages import constants as messages

# load the geoluminate.yml configuration file
config = os.getenv("GEOLUMINATE_CONFIG_PATH", os.path.join(BASE_DIR, "geoluminate.yml"))

sys.path.append(os.path.join(BASE_DIR, "project", "schemas"))  # at the bottom of the file


with open(config) as f:
    GEOLUMINATE = yaml.safe_load(f)

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    DJANGO_SECRET_KEY=(str, "HoVcnlU2IqQN1YqvsY7dQ1xtdhLavAeXn1mUEAI0Wu8vkDbodEqRKkJbHyMEQS5F"),
    SHOW_DEBUG_TOOLBAR=(bool, False),
    CACHE=(bool, False),
)


# print(env("COMPRESS_ENABLED"))

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(BASE_DIR / ".env"))

# SECRET_KEY = os.environ.get("SECRET_KEY")

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY")

# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "UTC"
""""""

SITE_NAME = GEOLUMINATE["database"]["name"]

META_SITE_NAME = SITE_NAME

# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1


# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "0.0.0.0"]

# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [(admin["name"], admin["email"]) for admin in GEOLUMINATE["application"]["developers"]]
MANAGERS = ADMINS

# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "geoluminate.urls"

# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"


# Coloured Messages
MESSAGE_TAGS = {
    messages.DEBUG: "debug alert-secondary",
    messages.INFO: "info alert-info",
    messages.SUCCESS: "success alert-success",
    messages.WARNING: "warning alert-warning",
    messages.ERROR: "error alert-danger",
}

# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

TAGGIT_CASE_INSENSITIVE = True

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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
                "geoluminate.context_processors.global_config",
                "cms.context_processors.cms_settings",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        },
    },
]

GEOLUMINATE_APPS = [
    # Admin apps
    "adminactions",
    "geoluminate.contrib.admin",
    "jazzmin",
    "postgres_metrics.apps.PostgresMetrics",
    "polymorphic",
    "modeltranslation",
    # core Django apps
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    "django.contrib.gis",
    "django.contrib.humanize",
    # "django.forms",
    "drf_auto_endpoint",
    # "auto_datatables.apps.AutoDataTablesConfig",
    # required by geoluminate
    "geoluminate",
    "geoluminate.contrib.project",
    "geoluminate.contrib.controlled_vocabulary",
    "geoluminate.contrib.user",
    "geoluminate.contrib.api",
    "geoluminate.contrib.gis",
    "geoluminate.contrib.literature",
    "auto_datatables",
    # "ror",
    # authentication
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.orcid",
    "invitations",
    # required by django cms
    "cms",
    "menus",
    "sekizai",
    "treebeard",
    # required by djangocms-frontend
    "djangocms_text_ckeditor",
    "filer",
    "easy_thumbnails",
    "djangocms_frontend",
    "djangocms_frontend.contrib.accordion",
    "djangocms_frontend.contrib.alert",
    "djangocms_frontend.contrib.badge",
    "djangocms_frontend.contrib.card",
    "djangocms_frontend.contrib.carousel",
    "djangocms_frontend.contrib.collapse",
    "djangocms_frontend.contrib.content",
    "djangocms_frontend.contrib.grid",
    "djangocms_frontend.contrib.image",
    "djangocms_frontend.contrib.jumbotron",
    "djangocms_frontend.contrib.link",
    "djangocms_frontend.contrib.listgroup",
    "djangocms_frontend.contrib.media",
    "djangocms_frontend.contrib.tabs",
    "djangocms_frontend.contrib.utilities",
    # APPS FOR DJANGO REST FRAMEWORK
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "drf_spectacular",  # auto documentation of API
    "drf_spectacular_sidecar",  # static files for drf_spectacular
    # "rest_framework_datatables_editor",
    # commenting system via django-fluent-comments[threadedcomment]
    "fluent_comments",
    "threadedcomments",
    "django_comments",
    "solo",  # singleton model for storing dynamic global variables in the DB
    "storages",  # for setting up backend storages
    "simple_menu",  # for defining non-CMS menus in the application
    # building nice looking forms and filters
    "django_filters",
    "crispy_forms",
    "crispy_bootstrap5",
    # some other useful apps that are required by the default installation
    "sortedm2m",  # sortable m2m relationships
    "django_htmx",  # context processor for dealing with htmx requests
    "django_celery_beat",  # celery based task manager
    "meta",  # for seo optimization
    "taggit",  # providing taggable keywords to any model
    "django_social_share",  # easy links to social sharing sites
    "import_export",  # for csv import and export via the admin site
    # 'import_export_celery',
    # not sure if these are explicitly needed or not
    # 'newsletter',
    # 'rest_framework_gis',
    # 'django_json_widget',  # provides a json form field for json_field
    "rosetta",  # in app translations
    # "controlled_vocabulary",  # a nice app for controlled vocabulary fields
    # "menu",  # is this supposed to be here?
    "django_select2",  # select2 widget integration with models
    "dbbackup",
    # "tellme",  # adds user feedback functionality to the site
    "django_spaghetti",  # entity-relationship diagrams
    # "jazzmin_translate",  # rosetta compatibility with jazzmin
    # "django_better_admin_arrayfield",  # nice admin widget for postgres array fields
    # GEOLUMINATE DEFAULT PLUGINS
    "literature",
    "formset",
    # research projects
    # research_projects
    # "licensing",
    # cataloguing of scientific instruments
    "laboratory",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "cms.middleware.utils.ApphookReloadMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "cms.middleware.user.CurrentUserMiddleware",
    "cms.middleware.page.CurrentPageMiddleware",
    "cms.middleware.toolbar.ToolbarMiddleware",
    "cms.middleware.language.LanguageCookieMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "geoluminate.middleware.GeoluminateLockdownMiddleware",
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

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS

STATICFILES_DIRS = [
    str(BASE_DIR / "project" / "static"),
]

# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [str(BASE_DIR / "project" / "locale")]

# Collect static and save media to the application base directory
# --------------------------------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(BASE_DIR / "static")

# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(BASE_DIR / "media")

if env("SHOW_DEBUG_TOOLBAR"):
    GEOLUMINATE_APPS.append("debug_toolbar")
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

    DEBUG_TOOLBAR_CONFIG = {
        "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
        "SHOW_TEMPLATE_CONTEXT": True,
    }

    # DEBUG_TOOLBAR_PANELS += [
    #     "template_profiler_panel.panels.template.TemplateProfilerPanel",
    # ]
