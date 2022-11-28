from django.db import models
from django.utils.translation import gettext as _, pgettext as _p
from solo.models import SingletonModel
from crossref.conf import settings


class Configuration(SingletonModel):

    KEPLER_LANG_CODES = [
        ('en', _('English')),
        ('fi', _('Finish')),
        ('pt', _('Portuguese')),
        ('ca', _('Catalan')),
        ('es', _('Spanish')),
        ('ja', _('Japanese')),
        ('cn', _('Chinese')),
        ('ru', _('Russian')),
    ]

    VERSIONS = [("v1", "v1")]
    THEMES = [
        ("dark", _("Dark")),
        ("light", _("Light")),
        ("base", _("Base")),
    ]

    mapbox_token = models.CharField(_('Mapbox API token'),
                                    help_text=_(
                                        'Public Mapbox API token to use with kepler.gl. The application will not work until this has been supplied.'),
                                    max_length=255,
                                    blank=True, null=True)

    mapState = models.JSONField(_('map state'),
                                help_text=_(
                                    'Configuration object for the map state'),
                                default=dict)

    mapStyle = models.JSONField(_('map style'),
                                help_text=_(
                                    'Configuration object for the map style'),
                                default=dict)

    visState = models.JSONField(_('visual state'),
                                help_text=_(
                                    'Configuration object for the visual state'),
                                default=dict)

    version = models.CharField(_('version'),
                               max_length=2,
                               help_text=_(
                                   'Kepler version. Currently only v1 is supported.'),
                               choices=VERSIONS,
                               default='v1')

    theme = models.CharField(_('Preferred theme'),
                             max_length=5,
                             help_text=_(
                                 'The preferred theme to use. Note that preference is given to the browsers prefers-color-scheme setting.'),
                             choices=THEMES,
                             default='dark')

    lang = models.CharField(_('Kepler fallback language'),
                            max_length=2,
                            help_text=_(
                                'The fallback language to use if the user\'s current locale is not supported by Kepler.'),
                            choices=KEPLER_LANG_CODES,
                            default='en')

    def __str__(self):
        return _("Configuration")

    class Meta:
        verbose_name = _("Configuration")

    def build_config(self):
        return {
            'config': {
                'mapState': self.mapState,
                'mapStyle': self.mapStyle,
                'visState': self.visState,
            },
            'version': self.version,
        }
