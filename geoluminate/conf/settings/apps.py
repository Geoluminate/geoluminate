GEOLUMINATE_APPS = [
    # Admin apps
    # "djangocms_admin_style",
    "geoluminate.contrib.admin",
    # "adminactions",
    # "jazzmin",
    "polymorphic",
    # "modeltranslation",
    # DJANGO CORE
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.admin",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    "django.contrib.gis",
    "django.contrib.humanize",
    # GEOLUMINATE CORE
    "geoluminate",
    "geoluminate.contrib.core",
    "geoluminate.contrib.configuration",
    "geoluminate.contrib.projects",
    "geoluminate.contrib.datasets",
    "geoluminate.contrib.reviews",
    "geoluminate.contrib.samples",
    "geoluminate.contrib.users",
    "geoluminate.contrib.organizations",
    "auto_datatables",
    # AUTHENTICATION AND USERS
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.orcid",
    "invitations",
    # "organizations",
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
    "djangocms_frontend.contrib.icon",
    "djangocms_frontend.contrib.image",
    "djangocms_frontend.contrib.jumbotron",
    "djangocms_frontend.contrib.link",
    "djangocms_frontend.contrib.listgroup",
    "djangocms_frontend.contrib.media",
    "djangocms_frontend.contrib.tabs",
    "djangocms_frontend.contrib.utilities",
    "geoluminate.contrib.contributors",
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
    # OTHERS
    "actstream",
    "solo",  # singleton model for storing dynamic global variables in the DB
    "django_contact_form",  # for contact forms
    "storages",  # for setting up backend storages
    "simple_menu",  # for defining non-CMS menus in the application
    # building nice looking forms and filters
    "django_filters",
    "crispy_forms",
    "crispy_bootstrap5",
    # some other useful apps that are required by the default installation
    "django_celery_beat",  # celery based task manager
    "meta",  # for seo optimization
    "taggit",  # providing taggable keywords to any model
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
    # "django_better_admin_arrayfield",  # nice admin widget for postgres array fields
    # GEOLUMINATE DEFAULT PLUGINS
    "literature",
    "formset",
    "licensing",
    "laboratory",  # cataloguing of scientific instruments
    "research_vocabs",
]


if SHOW_DEBUG_TOOLBAR:
    GEOLUMINATE_APPS.append("debug_toolbar")
