from django.db import models
from django.utils.http import urlquote_plus
from django.utils.translation import gettext as _, pgettext as _p
from django.utils.html import mark_safe
from taggit.managers import TaggableManager
from django.urls import reverse
from django.apps import apps 
from django.contrib.auth import get_user_model
import crossref.models as cr_models
from django.contrib.gis.db.models import Extent 

Author = cr_models.Author

class Publication(cr_models.Work):
    pdf = models.FileField(upload_to='publications/', blank=True, null=True)
    owner = models.ForeignKey(get_user_model(), 
        verbose_name=_('owner'),
        related_name='publications',
        blank=True, null=True,
        on_delete=models.SET_NULL)

    verified_by = models.ManyToManyField("user.User",
        related_name='verifications', blank=True)

    bibtex = models.TextField(blank=True,null=True)
    keywords = TaggableManager( 
        blank=True,
        verbose_name=_('key words'), help_text=None)

    _metadata = {
        'title': 'get_meta_title',
        'description': 'get_meta_description',
        'authors': 'display_authors',
        'year': 'year',
        }

    def get_data(self,data_type=None):
        return dict(
            intervals = self.intervals.all(),
            temperature = self.temperature_logs.all(),
            conductivity = self.conductivity_logs.all(),
            )

    def get_absolute_url(self):
        return reverse("publications:detail", kwargs={"pk": self.pk})

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

    def bbox(self):
        return self.sites.aggregate(Extent('geom'))['geom_extent']
