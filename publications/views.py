from publications.models import Publication
from django.views.generic import DetailView
from thermoglobe.mixins import DownloadMixin 
from meta.views import MetadataMixin
from django_filters.views import FilterView
from .filters import PublicationFilter
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from thermoglobe.models import Site
from django.contrib import auth
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.shortcuts import get_current_site
from thermoglobe.tables import IntervalTable, HeatProductionTable, ConductivityTable, TemperatureTable, SiteTable
from crossref.views import PublicationPaginateYearView


@login_required
def verify(request, pk):
    pub = get_object_or_404(Publication, pk=pk)
    pub.is_verified = True
    pub.verified_by.add(request.user)
    pub.save()
    return redirect(reverse('publications:detail',kwargs={'pk':pk}))


@login_required
def claim(request, pk):
    pub = get_object_or_404(Publication, pk=pk)
    subject = render_to_string("emails/publication_claim_subject.txt")

    subject = "".join(subject.splitlines())
    message = render_to_string("emails/publication_claim_body.txt", 
        context=dict(
            scheme = "https" if request.is_secure() else "http",
            site = get_current_site(request),
            publication=pub,
        ),
        request=request)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,['admin@geoluminate.com.au'],fail_silently=False)

    return redirect(reverse('publications:detail', kwargs={'pk':pub.pk}))


@login_required
def claim_confirmed(request):
    user = get_object_or_404(auth.get_user_model(),pk=request.GET.get('user_id'))
    pub = get_object_or_404(Publication, pk=request.GET.get('pub_id'))
    user.publications.add(pub)
    return redirect(reverse('publications:detail',kwargs={'pk':request.GET.get('pub_id')}))


class PublicationListView(PublicationPaginateYearView, FilterView):
    model = Publication
    template_name = 'crossref/publication_list.html'
    paginate_by = 50
    filterset_class = PublicationFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)      
        if self.filterset_class:
            context['parameters'] = self.get_filter_parameters()
        return context

    def get_queryset(self):
        return super().get_queryset().prefetch_related('author','sites', 'intervals','temperature_logs','conductivity_logs','heat_production_logs').exclude(published__year__isnull=True)


class PublicationDetailsView(DownloadMixin, MetadataMixin, DetailView):
    template_name = "thermoglobe/publication_details.html"
    model = Publication

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tables'] = [
            SiteTable(self.get_object()), 
            # IntervalTable(self.get_object()), 
            # TemperatureTable(self.get_object()), 
            # HeatProductionTable(self.get_object()), 
            # ConductivityTable(self.get_object())
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

