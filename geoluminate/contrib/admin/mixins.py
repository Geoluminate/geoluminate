import zipfile
from datetime import datetime as dt
from io import StringIO

from django.contrib.gis import admin
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from geoluminate.contrib.literature.models import Publication

# from simple_history.admin import SimpleHistoryAdmin


class BaseAdmin(admin.OSMGeoAdmin):
    def name(self, obj):
        return obj._name

    name.admin_order_field = "_name"  # type: ignore[attr-defined]

    def site_operator(self, obj):
        return obj._operator

    site_operator.admin_order_field = "_operator"  # type: ignore[attr-defined]

    def reference(self, obj):
        return obj._reference

    reference.admin_order_field = "_reference"  # type: ignore[attr-defined]

    def sites(self, obj):
        return obj._site_count

    sites.admin_order_field = "_site_count"  # type: ignore[attr-defined]

    def edit(self, obj):
        return mark_safe('<i class="fas fa-edit"></i>')  # noqa: S308

    edit.short_description = ""  # type: ignore[attr-defined]


class DownloadMixin:
    def get(self, request, *args, **kwargs):
        if "download" in request.GET:
            return self.download(request, *args, **kwargs)
        else:
            return super().get(self, request, *args, **kwargs)

    def download(self, request, *args, **kwargs):
        response, zf = self.prepare_zip_response(fname=self.get_object())

        Publication.objects.none()
        for key, qs in self.get_object().get_data().items():
            if key == "intervals" and qs.exists():
                # create a csv file and save it to the zip object
                zf.writestr(f"{key}.csv", qs.values_list().to_csv_buffer())
                # sites = DATABASE.objects.filter(**{f"{key}__in": qs})
            elif qs.exists():
                # create a csv file and save it to the zip object
                zf.writestr(f"{key}.csv", qs.explode_values().to_csv_buffer())
                # sites = DATABASE.objects.filter(**{f"{key}_logs__in": qs})

            # references = (
            #     references | Publication.objects.filter(sites__in=sites).distinct()
            # )

        # write references to .bib file
        # if references:
        #     zf.writestr(
        #         f"{self.get_object()}.bib", self.references_to_bibtex(references)
        #     )

        return response

    def references_to_bibtex(self, references):
        # add bibtex file to zip object
        references = references.distinct().exclude(bibtex__isnull=True).values_list("bibtex", flat=True)
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
