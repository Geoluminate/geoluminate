from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models
from shortuuid.django_fields import ShortUUIDField
from meta.models import ModelMeta
from django.conf import settings
from simple_history.models import HistoricalRecords
from polymorphic.models import PolymorphicModel


class Base(ModelMeta, PolymorphicModel):
    last_modified = models.DateTimeField(_('last modified'), auto_now=True)
    date_added = models.DateTimeField(_('date added'),
                                      auto_now_add=True,)
    comment = models.TextField(
        _("comment"),
        help_text=_(
            'General comments regarding the site and/or measurement'),
        blank=True, null=True)
    references = models.ManyToManyField("literature.Publication",
                                        verbose_name=_("references"),
                                        help_text=_(
                                            'The reference or publication from which the data were sourced. Each site may have multiple references.'),
                                        blank=True)
    date_acquired = models.DateTimeField(
        _('date acquired'),
        help_text=_(
            'Date when the data for the given site was acquired'),
        null=True,
    )
    pid = ShortUUIDField(
        length=10,
        blank=True,
        max_length=15,
        prefix="GHFS-",
        alphabet="23456789ABCDEFGHJKLMNPQRSTUVWXYZ",
    )

    _metadata = {
        'title': 'get_meta_title',
        'description': 'description',
        'year': 'year',
    }

    if not settings.DEBUG:
        history = HistoricalRecords()

    class Meta:
        abstract = True
