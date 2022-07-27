import uuid
from django.db import models
from django.utils.http import urlquote_plus
from django.utils.translation import gettext as _, pgettext as _p
from django.utils.html import mark_safe
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase
from django.urls import reverse
from django.apps import apps 
from django.contrib.auth import get_user_model
from ordered_model.models import OrderedModelBase
from sortedm2m.fields import SortedManyToManyField
from crossref.models import PublicationAbstract, AuthorAbstract


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

class Author(AuthorAbstract):
    pass 

class Publication(PublicationAbstract):
 
    owner = models.ForeignKey(get_user_model(), 
        verbose_name=_('owner'),
        related_name='publications',
        blank=True, null=True,
        on_delete=models.SET_NULL)
    source = models.CharField(max_length=128,
        default='User Upload',
        blank=True)

    verified_by = models.ManyToManyField("user.User",
        related_name='verifications', blank=True)
    keywords = TaggableManager(through=UUIDTaggedItem, 
        blank=True,
        verbose_name=_('key words'), help_text=None)
    abstract = models.TextField(blank=True)
    bibtex = models.TextField(blank=True,null=True)

    _metadata = {
        'title': 'get_meta_title',
        'description': 'get_meta_description',
        'authors': 'display_authors',
        'year': 'year',
        }

    class Meta(PublicationAbstract.Meta):
        db_table = 'publications'

        
    def get_data(self,data_type=None):
        return dict(
            intervals = self.intervals.all(),
            temperature = self.temperature_logs.all(),
            conductivity = self.conductivity_logs.all(),
            )

    def get_absolute_url(self):
        return reverse("publications:detail", kwargs={"pk": self.pk})

    def article(self):
        if self.DOI:
            return mark_safe('<a href="https://doi.org/{}"><i class="fas fa-globe fa-lg"></i></a>'.format(self.DOI))
        else:
            return ''

    def file_download(self):
        if self.file:
            return mark_safe('<a href="https://doi.org/{}"><i class="fas fa-globe fa-lg"></i></a>'.format(self.DOI))
        else:
            return ''

    def is_verified(self):
        return self.verified_by.exists()

    def keywords_escaped(self):
        return [(keyword.strip(), urlquote_plus(keyword.strip()))
            for keyword in self.keywords.split(',')]
