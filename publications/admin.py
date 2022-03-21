from django.contrib import admin
from .models import Publication 
from import_export.admin import ExportActionModelAdmin
from .resources import PublicationResource
from django.shortcuts import render
from grappelli.forms import GrappelliSortableHiddenMixin
from django.utils.translation import gettext as _
from django.shortcuts import render
from crossref.admin import PublicationAdminMixin
from .models import Author


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

admin.site.register(Author)
# class AuthorAdmin(ExportActionModelAdmin):
#     change_list_template = "admin/change_list_filter_sidebar.html"
#     change_list_filter_template = "admin/filter_listing.html"

#     list_display = ['family','given']
#     search_fields = ['family', 'given']
#     inlines = [PublicationInline]
#     fields = [('given','family')]

#     # def get_queryset(self, request):
#     #     return super().get_queryset(request)

#     def publications(self,obj):
#         return obj.publications.count()


