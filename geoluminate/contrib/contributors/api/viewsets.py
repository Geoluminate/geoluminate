from rest_framework import viewsets

from geoluminate.api.v1.serializers import ProjectSerializer
from geoluminate.contrib.contributors.models import Contributor
from geoluminate.contrib.datasets.models import Dataset
from geoluminate.contrib.projects.models import Project

from .serializers import ProfileSerializer


class ProfileViewset(viewsets.ReadOnlyModelViewSet):
    max_paginate_by = 1000
    serializer_class = ProfileSerializer
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
