from django.contrib.auth import get_user_model
from rest_framework import viewsets

from geoluminate.contrib.project.api.serializers import (
    DatasetSerializer,
    ProjectSerializer,
)
from geoluminate.contrib.project.models import Contributor, Dataset, Project

from ..models import Profile, User
from .serializers import ProfileSerializer, UserSerializer


class UserViewset(viewsets.ReadOnlyModelViewSet):
    max_paginate_by = 1000
    serializer_class = UserSerializer
    queryset = User.objects.select_related("profile").all()


class ProfileViewset(viewsets.ReadOnlyModelViewSet):
    max_paginate_by = 1000
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


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
    serializer_class = DatasetSerializer
    queryset = Dataset.objects.all()

    def get_queryset(self):
        contributions = Contributor.objects.filter(
            profile=self.kwargs["contributor_pk"],
            content_type__model="dataset",
        )
        return self.queryset.filter(contributors__in=contributions)
