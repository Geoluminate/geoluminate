from django.db import models
from django.utils.translation import gettext_lazy as _


class License(models.Model):
    uri = models.URLField(
        _("URI"),
        help_text=_("URI to an online published version of the license."),
        max_length=200, primary_key=True)
    name = models.CharField(_('name'),
                            help_text=_("Short form name of the license."),
                            max_length=32)
    about = models.TextField(_('about'),
                             help_text=_("Description of the license."))
    snippet = models.TextField(_('html snippet'),
                               help_text=_("HTML snippet for the license. Useful for display of Creative Commons licenses."))

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("License")
        verbose_name_plural = _("License")
        db_table = 'django_license'
