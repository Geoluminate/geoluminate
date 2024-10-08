INSTALLED_APPS = [
    # Admin apps
    # "adminactions",
    "admin_extra_buttons",
    # "modeltranslation",
    "admin_tools",
    "admin_tools.theming",
    "admin_tools.menu",
    "admin_tools.dashboard",
    # DJANGO CORE
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    # "django.contrib.gis",
    "django.contrib.humanize",
    "actstream",
    # "taggit",  # required from django-literature
    # GEOLUMINATE
    "geoluminate",
    "geoluminate.core",
    "geoluminate.identity",
    # "configuration",
    "geoluminate.contrib.projects",
    "geoluminate.contrib.datasets",
    "geoluminate.contrib.samples",
    "geoluminate.contrib.measurements",
    "geoluminate.contrib.contributors",
    # COMMENTING FRAMEWORK
    "django_comments_xtd",
    "django_comments",
    "polymorphic",
    "polymorphic_treebeard",
    "treebeard",
    "parler",
    # AUTHENTICATION AND USERS
    "account_management",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.orcid",
    "allauth.mfa",
    "allauth.usersessions",
    "invitations",
    # DJANGO REST FRAMEWORK
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "drf_spectacular",  # auto documentation of API
    "drf_spectacular_sidecar",  # static files for drf_spectacular
    "drf_auto_endpoint",
    # UTILITIES
    "sekizai",
    "easy_thumbnails",
    "easy_icons",
    "django_celery_beat",  # celery based task manager
    # OTHERS
    "solo",  # singleton model for storing dynamic global variables in the DB
    "django_contact_form",  # for contact forms
    "storages",  # for setting up backend storages
    "simple_menu",  # for defining non-CMS menus in the application
    # building nice looking forms and filters
    "django_filters",
    "crispy_forms",
    "crispy_bootstrap5",
    # some other useful apps that are required by the default installation
    "meta",  # for seo optimization
    "django_social_share",  # easy links to social sharing sites
    "django_bleach",  # for sanitizing html input
    "compressor",
    "django_htmx",
    "el_pagination",
    "django_select2",
    "client_side_image_cropping",
    "dbbackup",
    "webpack_loader",
    "imagekit",
    "image_uploader_widget",
    "literature",
    "formset",
    "licensing",
    "laboratory",
    "research_vocabs",
    "neapolitan",
    "template_partials.apps.SimpleAppConfig",
    "jsonfield_toolkit",
    "django_extensions",
    "flex_menu",
    "django_tables2",
    "django_setup_tools",
    *GEOLUMINATE_APPS,
]


# if SHOW_DEBUG_TOOLBAR:
#     INSTALLED_APPS.append("debug_toolbar")
