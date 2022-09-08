# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
from django.utils.translation import gettext_lazy as _


LANGUAGE_CODE = 'en'

TIME_ZONE = 'Australia/Adelaide'

USE_I18N = True

USE_L10N = True

ROSETTA_SHOW_AT_ADMIN_PANEL = True

# Instead of creating a global translators group, create individual per-language groups, e.g. translators-de, translators-fr, and assign users to these.
ROSETTA_LANGUAGE_GROUPS = True

ROSETTA_MESSAGES_PER_PAGE = 25

ROSETTA_EXCLUDED_APPLICATIONS = ['django',"allauth.account",]