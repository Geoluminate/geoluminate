from django.db import models
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel
from easy_thumbnails.fields import ThumbnailerField

class SiteConfiguration(SingletonModel):

    site_name = models.CharField(max_length=255, default='Site Name')
    logo = ThumbnailerField(null=True, blank=True, upload_to='logos')
    icon = ThumbnailerField(null=True, blank=True, upload_to='logos')

    maintenance_mode = models.BooleanField(default=False)

    class Meta:
        db_table = 'site_config'
        verbose_name = _('site configuration')

    def __str__(self):
        return "Site Configuration"
