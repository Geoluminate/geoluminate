from cms.extensions import PageExtension
from cms.extensions.extension_pool import extension_pool
from django.utils.translation import gettext_lazy as _
from djangocms_icon.fields import Icon


class Icon(PageExtension):
    """Gives the ability to store icons with the Django CMS Page object"""
    icon = Icon(verbose_name=_('Icon'))

    class Meta:
        db_table = 'core_cms_icon'

    def __str__(self):
        return self.icon


extension_pool.register(Icon)
