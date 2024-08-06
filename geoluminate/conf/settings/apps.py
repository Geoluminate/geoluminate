GEOLUMINATE_APPS = [
    # Admin apps
    # "adminactions",
    # "jazzmin",
    # "modeltranslation",
    # DJANGO CORE
    "django.contrib.admin",
    "django.contrib.auth",
    "polymorphic",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    "django.contrib.gis",
    "django.contrib.humanize",
    "actstream",
    # COMMENTING FRAMEWORK
    "fluent_comments",
    "threadedcomments",
    "django_comments",
    "taggit",  # providing taggable keywords to any model
    # GEOLUMINATE CORE
    "geoluminate",
    "geoluminate.contrib.core",
    "geoluminate.contrib.configuration",
    "geoluminate.contrib.projects",
    "geoluminate.contrib.datasets",
    "geoluminate.contrib.reviews",
    "geoluminate.contrib.samples",
    "geoluminate.contrib.measurements",
    "geoluminate.contrib.contributors",
    "geoluminate.contrib.users",
    "geoluminate.contrib.organizations",
    "auto_datatables",
    # AUTHENTICATION AND USERS
    "account_management",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.orcid",
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
    # "rest_framework_datatables_editor",
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
    # not sure if these are explicitly needed or not
    "compressor",
    # 'newsletter',
    # 'rest_framework_gis',
    "django_htmx",
    "el_pagination",
    "django_select2",  # select2 widget integration with models
    "client_side_image_cropping",
    "dbbackup",
    "webpack_loader",
    "imagekit",
    "image_uploader_widget",
    # GEOLUMINATE DEFAULT PLUGINS
    "literature",
    "formset",
    "licensing",
    "laboratory",  # cataloguing of scientific instruments
    "research_vocabs",
    "neapolitan",
    "template_partials",
]


if SHOW_DEBUG_TOOLBAR:
    GEOLUMINATE_APPS.append("debug_toolbar")
