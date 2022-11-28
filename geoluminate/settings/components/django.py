import os
from django.contrib.messages import constants as messages

DEBUG = True if os.environ.get('DEBUG') == 'TRUE' else False


BASE_DIR = os.getcwd()


SECRET_KEY = os.environ.get('SECRET_KEY')

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

USE_TZ = True

SITE_ID = 1

INTERNAL_IPS = ['127.0.0.1', ]

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

X_FRAME_OPTIONS = 'SAMEORIGIN'

# Coloured Messages
MESSAGE_TAGS = {
    messages.DEBUG: 'debug alert-secondary',
    messages.INFO: 'info alert-info',
    messages.SUCCESS: 'success alert-success',
    messages.WARNING: 'warning alert-warning',
    messages.ERROR: 'error alert-danger',
}


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


TAGGIT_CASE_INSENSITIVE = True


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
                'django.template.context_processors.tz',
                'sekizai.context_processors.sekizai',
                'django.template.context_processors.static',
                'geoluminate.context_processors.global_config',
                'cms.context_processors.cms_settings',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
            ],
        },
    },
]

INSTALLED_APPS = [
    'geoluminate.admin_tools',
    'grappelli.dashboard',
    'grappelli',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.gis',
    'geoluminate',
    'user',
    'django.contrib.humanize',
    # 'django.contrib.admindocs',
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.orcid",
    "invitations",
    'organizations',
    'cms',
    'geoluminate.cms',

    'menus',
    'sekizai',
    'treebeard',

    'djangocms_text_ckeditor',
    'filer',
    'easy_thumbnails',
    'djangocms_file',
    'djangocms_icon',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_bootstrap5',
    'djangocms_bootstrap5.contrib.bootstrap5_card',
    'djangocms_bootstrap5.contrib.bootstrap5_carousel',
    'djangocms_bootstrap5.contrib.bootstrap5_collapse',
    'djangocms_bootstrap5.contrib.bootstrap5_content',
    'djangocms_bootstrap5.contrib.bootstrap5_grid',
    'djangocms_bootstrap5.contrib.bootstrap5_jumbotron',
    'djangocms_bootstrap5.contrib.bootstrap5_link',
    'djangocms_bootstrap5.contrib.bootstrap5_listgroup',
    'djangocms_bootstrap5.contrib.bootstrap5_media',
    'djangocms_bootstrap5.contrib.bootstrap5_picture',
    'djangocms_bootstrap5.contrib.bootstrap5_tabs',
    'djangocms_bootstrap5.contrib.bootstrap5_utilities',
    'djangocms_video',

    "django_celery_beat",
    'solo',
    'django_extensions',
    'django_filters',
    'taggit',
    'storages',
    'crispy_forms',
    'crispy_bootstrap5',
    'fluent_comments',
    'threadedcomments',
    'django_comments',
    'django_social_share',
    'meta',
    "sortedm2m",
    "django_gravatar",
    "django_ckeditor_5",
    'django_htmx',
    'crossref',
    'crossref.cms',

    # GeoLuminate Apps
    'kepler',
    'literature',
    'theme',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    "django_htmx.middleware.HtmxMiddleware",
]

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
    'template_profiler_panel.panels.template.TemplateProfilerPanel',
]

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['outdent', 'indent', '|', 'bold', 'italic', 'underline', 'strikethrough',
                    'subscript', 'superscript', '|',
                    'bulletedList', 'numberedList',
                    ]
    },
}

CROSSREF_MODELS = {
    "work": "literature.Publication",
}


if os.getenv('DJANGO_ENV') == 'development':

    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    DATABASES = {
        'default': {
            'CONN_MAX_AGE': 0,
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USERNAME'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': 'localhost',
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
        },
        # 'default': {
        #     'ENGINE': 'django.db.backends.sqlite3',
        #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # }
    }
else:
    import django_heroku
    import dj_database_url
    STATICFILES_STORAGE = 'geoluminate.backends.storage.StaticStorage'
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_STATIC_LOCATION}/"

    SECURE_SSL_REDIRECT = True
    DATABASES = {
        'default': dj_database_url.config(
            conn_max_age=600,
            ssl_require=True)
    }
    django_heroku.settings(locals(), staticfiles=False)
    DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
