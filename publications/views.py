from publications.models import Publication, Author
from django.views.generic import DetailView
from main.mixins import DownloadMixin 
from meta.views import MetadataMixin
from django_filters.views import FilterView
from .filters import PublicationFilter
from database.models import Site
from django.utils.translation import gettext_lazy as _
from main.tables import SiteTable
from crossref.views import WorksByYearMixin
from django.shortcuts import render
from django.http import Http404
import time

class PublicationList(WorksByYearMixin):
    model = Publication
    template_name = 'publications/list.html'
    paginate_by = 50
    filterset_class = PublicationFilter

    def get_template_names(self):
        if self.request.htmx:
            # time.sleep(2)
            return ['crossref/partials/publication_list.html'] # The response HTML to inject into a list
        else:
            return [self.template_name] # The actual form


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)      
        if self.filterset_class:
            context['parameters'] = self.get_filter_parameters()
        return context

    def get_queryset(self):
        return super().get_queryset()

    def get_filter_parameters(self):
        """Gets url parameters from the filter and returns as a string to be placed behind paginator links"""
        request_copy = self.request.GET.copy()
        request_copy.pop('page', True)
        if request_copy:
            return '&'+request_copy.urlencode()
        else:
            return ''


class PublicationDetail(DownloadMixin, MetadataMixin, DetailView):
    template_name = "main/publication_details.html"
    model = Publication

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tables'] = [
            SiteTable(self.get_object()),
            ]
        return context

    def download(self, request, *args, **kwargs):
        response, zf = self.prepare_zip_response(fname=self.get_object())

        references = Publication.objects.none()
        for key, qs in self.get_object().get_data().items():
            if key == 'intervals' and qs.exists():
                # create a csv file and save it to the zip object
                zf.writestr(f"{key}.csv", qs.values_list().to_csv_buffer())
                sites = Site.objects.filter(**{f"{key}__in":qs})
            elif qs.exists():
                # create a csv file and save it to the zip object
                zf.writestr(f"{key}.csv", qs.explode_values().to_csv_buffer())
                sites = Site.objects.filter(**{f"{key}_logs__in":qs})

            references = references | Publication.objects.filter(sites__in=sites).distinct()
        
        # write references to .bib file
        if references:
            zf.writestr(f'{self.get_object()}.bib', self.references_to_bibtex(references))

        return response


class AuthorDetail(DownloadMixin, MetadataMixin, DetailView):
    template_name = "main/author_detail.html"
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['tables'] = [
        #     SiteTable(self.get_object()),
        #     ]
        return context
