from django.contrib import admin
from .models import Publication 
from import_export.admin import ExportActionModelAdmin
from .resources import PublicationResource
from django.shortcuts import render
from grappelli.forms import GrappelliSortableHiddenMixin
from django.utils.translation import gettext as _
from django.shortcuts import render
from crossref.admin import PublicationAdminMixin, AuthorAdminMixin
from .models import Author
from django.db.models import Count, Min, Max


class PublicationInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = Publication.author.through
    verbose_name = _("publication")
    verbose_name_plural = _("Publications")
    fields = ("publication", 'year', "title", 'journal', "position",)
    readonly_fields = ['title','year','journal']


    raw_id_fields = ('publication',)
    autocomplete_lookup_fields = {
        'fk': ['publication'],
    }
    extra=0

    def title(self, instance):
        return instance.publication.title
    title.short_description = _('title')

    def year(self, instance):
        return instance.publication.year
    year.short_description = _('year')

    def journal(self, instance):
        return instance.publication.container_title
    journal.short_description = _('journal/book title')

@admin.register(Publication)
class PublicationAdmin(PublicationAdminMixin, ExportActionModelAdmin):
    change_list_template = "admin/crossref/change_list_filter_sidebar.html"
    # change_list_filter_template = "admin/filter_listing.html"
    resource_class = PublicationResource
    list_display = ['file','article', 'label', 'title', 'container_title', 'is_referenced_by_count', 'published','issue','volume','page','type', '_sites']

    fieldsets = [
        (None, {
            'fields':[
                'pdf',
                ]}
            ),
        ('Bibliographic', {'fields':[
            'DOI',
            ('type', 'published'),
            'title',
            'author',
            'container_title',
            'volume',
            'issue',
            'page',
            'abstract',
            ]}),
        ('Additional', {'fields':[
            'keywords',
            'language',
            'source',
            'bibtex',
            ]}),
        ]


    def get_queryset(self, request):
        return (super().get_queryset(request)
            .prefetch_related('sites')
            .annotate(
                _sites=Count('sites'),
                )
        )

    def _sites(self, obj):
        return obj._sites
    _sites.admin_order_field = '_sites'
    _sites.short_description = _('heat flow sites')



# admin.site.register(Author)
@admin.register(Author)
class AuthorAdmin(AuthorAdminMixin, ExportActionModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"
    change_list_filter_template = "admin/filter_listing.html"

    inlines = [PublicationInline]
    fields = [('given','family')]
    actions = ["merge",]

    # def get_queryset(self, request):
    #     return super().get_queryset(request)

    def publications(self,obj):
        return obj.publications.count()


