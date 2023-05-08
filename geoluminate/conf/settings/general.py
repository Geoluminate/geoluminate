import os

from django.contrib.messages import constants as messages

BASE_DIR = os.getcwd()


SECRET_KEY = os.environ.get("SECRET_KEY")


# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1


INTERNAL_IPS = [
    "127.0.0.1",
]

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
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
    # geoluminate configuration and user accounts
    "geoluminate",
    "geoluminate.contrib.user",
    "geoluminate.contrib.api",
    "geoluminate.contrib.literature",
    # "ror",
    # authentication
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.orcid",
    "invitations",
    # installed by django cms
    "cms",
    "menus",
    "sekizai",
    "treebeard",
    # installed by djangocms-frontend
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
    "drf_auto_endpoint",
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
    # 'geoluminate.contrib.gis', # do i need this here?
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
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


# MEDIA
# ------------------------------------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"


# if os.getenv("DJANGO_ENV") == "development":

#     STATIC_ROOT = os.path.join(BASE_DIR, "static")
#     MEDIA_ROOT = os.path.join(BASE_DIR, "media")
