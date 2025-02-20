from rest_framework import viewsets

from fairdm.contrib.api.serializers import ProjectSerializer
from fairdm.contrib.contributors.models import Contributor
from fairdm.core.models import Dataset, Project

from ..filters import ContributorFilter
from .serializers import ContributorPolymorphicSerializer


class ContributorViewset(viewsets.ReadOnlyModelViewSet):
    max_paginate_by = 1000
    # filterset_fields = ["name"]  # Fields to filter
    filterset_class = ContributorFilter
    serializer_class = ContributorPolymorphicSerializer
    queryset = Contributor.objects.all()


class ContributorProjectViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def get_queryset(self):
        contributions = Contributor.objects.filter(
            profile=self.kwargs["contributor_pk"],
            content_type__model="project",
        )
        return self.queryset.filter(contributors__in=contributions)


class ContributorDatasetViewset(viewsets.ReadOnlyModelViewSet):
    max_paginate_by = 1000
    serializer_class = ProjectSerializer
    queryset = Dataset.objects.all()

    def get_queryset(self):
        contributions = Contributor.objects.filter(
            profile=self.kwargs["contributor_pk"],
            content_type__model="dataset",
        )
        return self.queryset.filter(contributors__in=contributions)
