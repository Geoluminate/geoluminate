import os

GEOLUMINATE_APPS = [
    # Admin apps
    # "djangocms_admin_style",
    "adminactions",
    "jazzmin",
    "postgres_metrics.apps.PostgresMetrics",
    "polymorphic",
    "modeltranslation",
    # DJANGO CORE
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
    # GEOLUMINATE CORE
    "geoluminate",
    "geoluminate.contrib.core",
    "geoluminate.contrib.user",
    "auto_datatables",
    # AUTHENTICATION AND USERS
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.orcid",
    "invitations",
    "organizations",
    # DJANGO CMS CORE
    "cms",
    "menus",
    "sekizai",
    "treebeard",
    # DJANGO CMS PLUGINS
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
    # DJANGO REST FRAMEWORK
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "drf_spectacular",  # auto documentation of API
    "drf_spectacular_sidecar",  # static files for drf_spectacular
    "drf_auto_endpoint",
    # "rest_framework_datatables_editor",
    # COMMENTING FRAMEWORK
    "fluent_comments",
    "threadedcomments",
    "django_comments",
    "solo",  # singleton model for storing dynamic global variables in the DB
    "django_contact_form",  # for contact forms
    "storages",  # for setting up backend storages
    "simple_menu",  # for defining non-CMS menus in the application
    # building nice looking forms and filters
    "django_filters",
    "crispy_forms",
    "crispy_bootstrap5",
    # some other useful apps that are required by the default installation
    "sortedm2m",  # sortable m2m relationships
    # "django_htmx",  # context processor for dealing with htmx requests
    "django_celery_beat",  # celery based task manager
    "meta",  # for seo optimization
    "taggit",  # providing taggable keywords to any model
    "django_social_share",  # easy links to social sharing sites
    # "import_export",  # for csv import and export via the admin site
    "django_bleach",  # for sanitizing html input
    # 'import_export_celery',
    # not sure if these are explicitly needed or not
    # 'newsletter',
    # 'rest_framework_gis',
    # 'django_json_widget',  # provides a json form field for json_field
    # "rosetta",  # in app translations
    # "menu",  # is this supposed to be here?
    "django_select2",  # select2 widget integration with models
    # "client_side_image_cropping",
    "dbbackup",
    # "tellme",  # adds user feedback functionality to the site
    "django_spaghetti",  # entity-relationship diagrams
    # "jazzmin_translate",  # rosetta compatibility with jazzmin
    # "django_better_admin_arrayfield",  # nice admin widget for postgres array fields
    # GEOLUMINATE DEFAULT PLUGINS
    "literature",
    "formset",
    # "licensing",
    "laboratory",  # cataloguing of scientific instruments
]


if os.environ.get("SHOW_DEBUG_TOOLBAR", False):
    GEOLUMINATE_APPS.append("debug_toolbar")
