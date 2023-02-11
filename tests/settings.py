"""
Django settings for example project.

"""
from geoluminate.conf import geoluminate_setup
from geoluminate.conf.global_settings import *

SECRET_KEY = "g8ktwj_nj0s*h54*$rfmg19rdzi@cam5xh!wfh&g9#bvnfhcos"

DEBUG = True

# Application definition
ROOT_URLCONF = "tests.urls"

WSGI_APPLICATION = "tests.wsgi.application"

BASE_MODEL = "geoluminate.contrib.gis.base.AbstractSite"
DATABASE_NAME = "Global Heat Flow Database"
DATABASE_ACRONYM = "GHFDB"
KEYWORDS = [
    "heat flow",
    "geothermal",
    "geoenergy",
]
GOVERNING_BODY = "International Heat Flow Commission"
GOVERNING_BODY_ACRONYM = "IHFC"
GOVERNING_BODY_WEBSITE = "ihfc.org"

INSTALLED_APPS = [
    "adminactions",
] + INSTALLED_APPS


INSTALLED_APPS += [
    "tellme",
    "django_spaghetti",
    "jazzmin_translate",
    "import_export",
    "django_better_admin_arrayfield",
]

SPAGHETTI_SAUCE = {
    "apps": ["filer", "user", "account", "socialaccount", "ror"],
    "show_fields": False,
    # "exclude": {"auth": ["user"]},
}

geoluminate_setup(globals())
