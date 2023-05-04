from django.shortcuts import get_object_or_404
from literature.models import Author
from rest_framework import viewsets
from rest_framework.response import Response

from geoluminate.contrib.api.v1.serializers import GeoFeatureSerializer
from geoluminate.contrib.api.v1.views import DataViewSet

# from geoluminate.utils import DATABASE
from geoluminate.utils.drf import DjangoFilterBackend

from ..models import Publication
from .serialize import AuthorSerializer, CoreNestedSerializer, LiteratureSerializer


class LiteratureView(viewsets.ReadOnlyModelViewSet):
    """API endpoint to request a set of  publications."""

    max_paginate_by = 1000
    pagination_class = None
    serializer_class = LiteratureSerializer
    filterset_fields = ["container_title", "published"]
    filter_backends = (DjangoFilterBackend,)
    queryset = Publication.objects.all()


class AuthorView(viewsets.ReadOnlyModelViewSet):
    """API endpoint to request a set of  publications."""

    serializer_class = AuthorSerializer
    queryset = Author.objects.with_work_counts()


class NestedAuthorList(AuthorView):
    def list(self, request, *args, **kwargs):
        pk = kwargs.pop("lit_pk")
        if pk:
            queryset = self.get_queryset().filter(works__pk=pk)
            serializer = self.get_serializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        pk = kwargs.pop("lit_pk")
        if pk:
            queryset = self.get_queryset().filter(works__pk=pk)
            instance = get_object_or_404(queryset, pk=pk)
            serializer = self.get_serializer(instance, context={"request": request})
        return Response(serializer.data)


class CoreNestedViewSet(DataViewSet):
    serializer_class = CoreNestedSerializer
    # queryset = DATABASE.objects.all()

    # def get_serializer_class(self):
    #     return self.serializer_class

    def list(self, request, *args, **kwargs):
        qs = self.queryset.objects.filter(references__pk=kwargs.pop("lit_pk"))

        if self.is_geojson():
            serializer = GeoFeatureSerializer(qs, many=True)
            # return Response(serializer.data)
        else:
            serializer = self.get_serializer(qs, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.queryset.objects.filter(pk=pk, references__pk=kwargs.pop("lit_pk"))
        instance = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(instance, context={"request": request})
        return Response(serializer.data)
