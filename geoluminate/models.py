from django.db import models
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel
from filer.fields.image import FilerImageField
from django.utils.encoding import force_str
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
# from .utils import get_dynamic_choice_enum
import importlib
from django.conf import settings


def import_attribute(path):
    assert isinstance(path, str)
    pkg, attr = path.rsplit(".", 1)
    ret = getattr(importlib.import_module(pkg), attr)
    return ret


def get_dynamic_choice_enum():
    path = getattr(settings, 'GEOLUMINATE_DYNAMIC_CHOICE_FIELDS', [])
    if path:
        return import_attribute(path)
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


class Choice(models.Model):
    """This is a generic model for storing modifiable choices in a single table.
    Each `type` relates to a collection of choices that can be utilised by
    `django.db.models.ChoiceField` fields in other models.
    """

    type = models.CharField(_('type'),
                            choices=get_dynamic_choice_enum().choices,
                            max_length=16)
    code = models.CharField(_('code'), max_length=64)
    name = models.CharField(_('name'), max_length=128)
    description = models.TextField(_('description'),
                                   blank=True, null=True)

    class Meta:
        verbose_name = _('Choice')
        verbose_name_plural = _('Choices')
        unique_together = ('type', 'code')
        ordering = ['type', 'code']
        db_table = 'dynamic_choices'

    def __str__(self):
        return self.code

    @staticmethod
    def autocomplete_search_fields():
        # For Django Grappelli related lookups
        return ("name__icontains", "code__icontains",)
