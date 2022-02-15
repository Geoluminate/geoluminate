# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
from django.utils.translation import ugettext_lazy as _


LANGUAGE_CODE = 'en'

TIME_ZONE = 'Australia/Adelaide'

USE_I18N = True

USE_L10N = True

LANGUAGES = (
    ## Customize this
    ('en', _('English')),
)