import zipfile
from datetime import datetime as dt
from io import StringIO

from django.contrib.gis import admin
from django.http import HttpResponse
from django.utils.html import mark_safe
from django.utils.translation import gettext as _
from simple_history.admin import SimpleHistoryAdmin

from geoluminate.contrib.literature.models import Publication
from geoluminate.utils import DATABASE


class BaseAdmin(admin.OSMGeoAdmin, SimpleHistoryAdmin):
    def name(self, obj):
        return obj._name

    name.admin_order_field = "_name"

    def site_operator(self, obj):
        return obj._operator

    site_operator.admin_order_field = "_operator"

    def reference(self, obj):
        return obj._reference

    reference.admin_order_field = "_reference"

    def sites(self, obj):
        return obj._site_count

    sites.admin_order_field = "_site_count"

    def edit(self, obj):
        return mark_safe('<i class="fas fa-edit"></i>')

    edit.short_description = ""


class DownloadMixin:
    def get(self, request, *args, **kwargs):
        if "download" in request.GET.keys():
            return self.download(request, *args, **kwargs)
        else:
            return super().get(self, request, *args, **kwargs)

    def download(self, request, *args, **kwargs):
        response, zf = self.prepare_zip_response(fname=self.get_object())

        references = Publication.objects.none()
        for key, qs in self.get_object().get_data().items():
            if key == "intervals" and qs.exists():
                # create a csv file and save it to the zip object
                zf.writestr(f"{key}.csv", qs.values_list().to_csv_buffer())
                sites = DATABASE.objects.filter(**{f"{key}__in": qs})
            elif qs.exists():
                # create a csv file and save it to the zip object
                zf.writestr(f"{key}.csv", qs.explode_values().to_csv_buffer())
                sites = DATABASE.objects.filter(**{f"{key}_logs__in": qs})

            references = (
                references | Publication.objects.filter(sites__in=sites).distinct()
            )

        # write references to .bib file
        if references:
            zf.writestr(
                f"{self.get_object()}.bib", self.references_to_bibtex(references)
            )

        return response

    def references_to_bibtex(self, references):
        # add bibtex file to zip object
        references = (
            references.distinct()
            .exclude(bibtex__isnull=True)
            .values_list("bibtex", flat=True)
        )
        buffer = StringIO()
        buffer.write("\n\n".join(references))
        return buffer.getvalue()

    def prepare_zip_response(self, fname=None):
        # prepare the response for csv file
        response = HttpResponse(content_type="application/zip")
        if fname is None:
            fname = f"Thermoglobe_{dt.now().strftime('%d_%b_%Y')}"
        response["Content-Disposition"] = f'attachment; filename="{fname}.zip"'
        return response, zipfile.ZipFile(response, "w")