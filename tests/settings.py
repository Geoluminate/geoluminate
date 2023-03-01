"""
Django settings for example project.

"""
from geoluminate.conf import auto_setup
from geoluminate.conf.local_defaults import *

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

INSTALLED_APPS = [] + INSTALLED_APPS

INSTALLED_APPS += []

SPAGHETTI_SAUCE = {
    "apps": ["filer", "user", "account", "socialaccount", "ror"],
    "show_fields": False,
    # "exclude": {"auth": ["user"]},
}

auto_setup(globals())
