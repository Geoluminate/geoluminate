from rest_framework import viewsets
from literature.models import Publication
from literature.api.serialize import LiteratureSerializer, AuthorSerializer, CoreNestedSerializer
from geoluminate.rest_framework.utils import DjangoFilterBackend
from rest_framework_extensions.mixins import PaginateByMaxMixin
from crossref.models import Author
from geoluminate.utils import DATABASE
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import mixins
from geoluminate.api.v1.views import DataViewSet
from rest_framework_datatables_editor.filters import DatatablesFilterBackend


# class LiteratureView(viewsets.ModelViewSet):

class LiteratureView(viewsets.ReadOnlyModelViewSet):
    """API endpoint to request a set of  publications."""
    max_paginate_by = 1000
    serializer_class = LiteratureSerializer
    filterset_fields = ['container_title', 'published']
    filter_backends = (DjangoFilterBackend,)
    queryset = Publication.objects.prefetch_related('sites')


class AuthorView(viewsets.ReadOnlyModelViewSet):
    """API endpoint to request a set of  publications."""
    serializer_class = AuthorSerializer
    queryset = Author.objects.with_work_counts()


class NestedAuthorList(AuthorView):
    def list(self, request, *args, **kwargs):
        pk = kwargs.pop('lit_pk')
        if pk:
            queryset = self.get_queryset().filter(works__pk=pk)
            serializer = self.get_serializer(
                queryset, many=True, context={
                    'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        pk = kwargs.pop('lit_pk')
        if pk:
            queryset = self.get_queryset().filter(works__pk=pk)
            instance = get_object_or_404(queryset, pk=pk)
            serializer = self.get_serializer(
                instance, context={'request': request})
        return Response(serializer.data)


class CoreNestedViewSet(DataViewSet):
    serializer_class = CoreNestedSerializer
    queryset = DATABASE.objects.all()

    # def get_serializer_class(self):
    #     return self.serializer_class

    def list(self, request, *args, **kwargs):
        queryset = DATABASE.objects.filter(
            references__pk=kwargs.pop('lit_pk'))
        serializer = self.get_serializer(
            queryset, many=True, context={
                'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = DATABASE.objects.filter(
            pk=pk, references__pk=kwargs.pop('lit_pk'))
        instance = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(
            instance, context={'request': request})
        return Response(serializer.data)
