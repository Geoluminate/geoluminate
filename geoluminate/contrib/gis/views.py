from django.conf import settings
from django.http import JsonResponse
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _
from django.views.generic import DetailView, TemplateView
from django_select2.views import AutoResponseView
from meta.views import Meta

from geoluminate.conf import settings
from geoluminate.core.mixins import FieldSetMixin


class MapView(TemplateView):
    template_name = "gis/application.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        db_name = getattr(settings, "DATABASE_NAME")
        context["meta"] = Meta(
            title="Viewer",
            description=f"Interactive mapping application for querying data contained within the {db_name}",
            keywords=[],
        )
        return context


class SiteView(FieldSetMixin, DetailView):
    template_name = "geoluminate/database/site.html"
    # model = DATABASE
    fieldset = [
        (
            "Heat Flow",
            {
                "fields": [
                    "q",
                    "q_unc",
                    "explo_method",
                    "environment",
                    "explo_purpose",
                    "water_temp",
                    "q_comment",
                ]
            },
        ),
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meta"] = self.get_object().as_meta(self.request)
        context["fieldset"] = self.get_fieldset()
        return context

    def get_queryset(self):
        return super().get_queryset().prefetch_related("references")
