from django.conf import settings
from django.contrib import admin, messages
from django.contrib.admin.models import ContentType, LogEntry
from django.db.models import Count
from django.shortcuts import render
from django.utils.translation import gettext as _

# from crossref import models as cr_models
from django_super_deduper.merge import MergedModelInstance
from grappelli.forms import GrappelliSortableHiddenMixin

# from crossref.admin import WorkAdminMixin, AuthorAdminMixin
# from .models import Author, Publication

# class PublicationInline(GrappelliSortableHiddenMixin, admin.TabularInline):
#     model = Publication.author.through
#     verbose_name = _("publication")
#     verbose_name_plural = _("Publications")
#     fields = ("publication", 'year', "title", 'journal', "position",)
#     readonly_fields = ['title', 'year', 'journal']

#     raw_id_fields = ('publication',)
#     autocomplete_lookup_fields = {
#         'fk': ['publication'],
#     }
#     extra = 0

#     def title(self, instance):
#         return instance.publication.title
#     title.short_description = _('title')

#     def year(self, instance):
#         return instance.publication.year
#     year.short_description = _('year')

#     def journal(self, instance):
#         return instance.publication.container_title
#     journal.short_description = _('journal/book title')


# # admin.site.unregister(cr_models.Work)


# @admin.register(Publication)
# class PublicationAdmin(WorkAdminMixin):
#     list_editable = ['pdf', ]
#     list_display = [
#         'pdf',
#         'article',
#         'label',
#         'title',
#         'container_title',
#         'is_referenced_by_count',
#         'published',
#         'issue',
#         'volume',
#         'page',
#         'type',
#         # '_sites',
#     ]

#     fieldsets = [
#         (None, {
#             'fields': [
#                 'pdf',
#             ]}
#          ),
#         ('Bibliographic', {'fields': [
#             'DOI',
#             ('type', 'published'),
#             'title',
#             # 'author',
#             'container_title',
#             'volume',
#             'issue',
#             'page',
#             'abstract',
#         ]}),
#         ('Additional', {'fields': [
#             'keywords',
#             'language',
#             'source',
#             # 'bibtex',
#         ]}),
#     ]

#     def get_queryset(self, request):
#         return (super().get_queryset(request)
#                 # .prefetch_related('sites')
#                 # .annotate(
#                 # _sites=Count('sites'))
#                 )

#     def _sites(self, obj):
#         return obj._sites
#     _sites.admin_order_field = '_sites'
#     _sites.short_description = _('heat flow sites')


# # admin.site.unregister(cr_models.Author)


# @admin.register(Author)
# class AuthorAdmin(AuthorAdminMixin):
#     # change_list_template = "admin/change_list_filter_sidebar.html"
#     # change_list_filter_template = "admin/filter_listing.html"

#     # inlines = [PublicationInline]
#     actions = ["merge", ]

#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         return qs

#     def publications(self, obj):
#         return obj.publications.count()

#     def merge(self, request, qs):
#         to_be_merged = [str(x) for x in qs]
#         if len(to_be_merged) > 2:
#             to_be_merged = f"{', '.join(to_be_merged[:-1])} and {to_be_merged[-1]}"
#         else:
#             to_be_merged = ' and '.join(to_be_merged)
#         change_message = f"Merged {to_be_merged} into a single {qs.model._meta.verbose_name}"
#         merged = MergedModelInstance.create(qs.first(), qs[1:], keep_old=False)
#         LogEntry.objects.log_action(
#             user_id=request.user.pk,
#             content_type_id=ContentType.objects.get_for_model(qs.model).pk,
#             object_id=qs.first().pk,
#             object_repr=str(qs.first()),
#             action_flag=2,  # CHANGE
#             change_message=_(change_message),
#         )
#         self.message_user(request, change_message, messages.SUCCESS)
#     merge.short_description = _("Merge duplicate authors")
