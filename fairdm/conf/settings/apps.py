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
    # FAIRDM
    "fairdm",
    "fairdm.contrib.generic",
    "fairdm.contrib.contributors",
    "fairdm.contrib.import_export",
    "fairdm.core",
    "fairdm.utils",
    "fairdm.contrib.identity",
    "actstream",
    # "configuration",
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
    "corsheaders",
    "dj_rest_auth.registration",
    "dj_rest_auth",
    "drf_auto_endpoint",
    "drf_spectacular_sidecar",  # static files for drf_spectacular
    "drf_spectacular",  # auto documentation of API
    "rest_framework.authtoken",
    "rest_framework",
    # UTILITIES
    "django_better_admin_arrayfield",
    "pwa",  # github.com/silviolleite/django-pwa
    "compressor",
    "dbbackup",
    "django_bleach",  # for sanitizing html input
    # "django_celery_beat",  # celery based task manager
    "django_cotton.apps.SimpleAppConfig",
    "django_extensions",
    "django_setup_tools",
    "django_tables2",
    "easy_icons",
    "easy_thumbnails",
    "flex_menu",
    "jsonfield_toolkit",
    "meta",  # for seo optimization
    "neapolitan",
    "sekizai",
    "template_partials.apps.SimpleAppConfig",
    # OTHERS
    "solo",  # singleton model for storing dynamic global variables in the DB
    "django_contact_form",  # for contact forms
    "storages",  # for setting up backend storages
    # building nice looking forms and filters
    "django_filters",
    "crispy_forms",
    "crispy_bootstrap5",
    "widget_tweaks",
    "django_select2",
    "client_side_image_cropping",
    # some other useful apps that are required by the default installation
    "django_social_share",  # easy links to social sharing sites
    "django_htmx",
    "webpack_loader",
    "imagekit",
    "literature",
    # ADMIN TOOLS
    "image_uploader_widget",
    # "formset",
    "licensing",
    "laboratory",
    "research_vocabs",
    "ordered_model",
    "taggit",
    "import_export",
    *FAIRDM_APPS,
]
