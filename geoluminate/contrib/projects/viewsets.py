from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ReadOnlyModelViewSet

from geoluminate.api.utils import NestedViewset, api_doc

from .models import Project
from .serializers import ProjectSerializer


@extend_schema_view(
    list=extend_schema(description=api_doc(Project, "list")),
)
class ProjectViewset(ReadOnlyModelViewSet):
    """A project is a collection of datasets and associated metadata. The Project model
    is the top level model in the Geoluminate schema heirarchy and all datasets, samples,
    sites and measurements should relate back to a project."""

    lookup_field = "uuid"
    max_paginate_by = 1000
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class NestedProjects(NestedViewset, ProjectViewset):
    """Adds the NestedViewSetMixin to the ProjectViewset to make sure that the queryset on nested routes is correctly filtered by the parent lookup fields."""

    pass
