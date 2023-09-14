from django.shortcuts import redirect
from django.template.loader import get_template, render_to_string
from drf_auto_endpoint.factories import serializer_factory
from drf_spectacular.utils import extend_schema, extend_schema_view

from geoluminate.api.viewsets import ViewsetMixin

from ..models import Dataset, Location, Project, Sample
from .serializers import (
    DatasetSerializer,
    LocationSerializer,
    MeasurementSerializer,
    ProjectSerializer,
    SampleSerializer,
)


@extend_schema_view(
    list=extend_schema(description=render_to_string("api/docs/project_list.md", context={"model": Project})),
)
class ProjectViewset(ViewsetMixin):
    """A project is a collection of datasets and associated metadata. The Project model
    is the top level model in the Geoluminate schema heirarchy and all datasets, samples,
    sites and measurements should relate back to a project."""

    template_name = "project/api.html"
    max_paginate_by = 1000
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        if request.accepted_renderer.format == "html":
            return redirect(self.get_object().get_absolute_url())
        return response


class DatasetViewset(ViewsetMixin):
    serializer_class = DatasetSerializer
    queryset = Dataset.objects.all()


class SampleViewset(ViewsetMixin):
    serializer_class = SampleSerializer
    queryset = Sample.objects.all()


class SiteViewset(ViewsetMixin):
    template_name = "project/api.html"
    max_paginate_by = 1000
    serializer_class = LocationSerializer
    queryset = Location.objects.all()


# class SiteMeasurement(ViewsetMixin):
#     # queryset = HeatFlow.objects.all()
#     serializer_class = MeasurementSerializer

#     def get_serializer_class(self):
#         serializer = self.serializer_class
#         serializer.Meta.model = self.queryset.model
#         return serializer
#         # if self.serializer_class:
#         #     return self.serializer_class
#         # return serializer_factory(model=self.queryset.model, base_class=MeasurementSerializer)


def MeasurementViewset(model):
    class MeasurementViewset(ViewsetMixin):
        queryset = model.objects.all()
        serializer_class = MeasurementSerializer

        def get_serializer_class(self):
            serializer = self.serializer_class
            serializer.Meta.model = self.queryset.model
            return serializer

    return MeasurementViewset


class SampleMeasurement(ViewsetMixin):
    model = None

    def get_queryset(self):
        return self.model.objects.all()
