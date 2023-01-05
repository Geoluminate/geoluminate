from django.db import models
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel
from filer.fields.image import FilerImageField
from django.utils.encoding import force_str
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from geoluminate.conf import settings
from django.utils.module_loading import import_string


def get_dynamic_choice_enum():
    path = getattr(settings, 'GEOLUMINATE_DYNAMIC_CHOICE_FIELDS', [])
    if path:
        return import_string(path)
    return models.TextChoices


class GlobalConfiguration(SingletonModel):

    site = models.OneToOneField(
        Site,
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    logo = FilerImageField(
        related_name='+',
        verbose_name=_('Logo'),
        null=True, blank=True, on_delete=models.SET_NULL)
    icon = FilerImageField(
        related_name='+',
        verbose_name=_('Icon'),
        null=True, blank=True, on_delete=models.SET_NULL)

    custodian = models.OneToOneField(
        to=get_user_model(),
        limit_choices_to={
            'is_staff': True,
        },
        verbose_name=_('custodian'),
        related_name='custodian',
        blank=True, null=True,
        on_delete=models.SET_NULL)

    class Meta:
        db_table = 'global_config'
        verbose_name = _('Global Configuration')

    def __str__(self):
        return force_str(_('Global Configuration'))


# imports the abstract base class specified in the settings
Base = import_string(getattr(settings, 'GEOLUMINATE_BASE_MODEL'))


class Geoluminate(Base):
    pass
