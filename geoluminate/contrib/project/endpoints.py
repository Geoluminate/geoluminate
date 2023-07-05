from rest_framework import serializers

from geoluminate import api
from geoluminate.contrib.gis.models import Site

from .models import Dataset, Project, Sample


@api.register
class ProjectEndpoint(api.Endpoint):
    model = Project
    include_str = False
    url = "projects"
    exclude_fields = ["datasets", "lead", "created_by"]


@api.register
class DatasetEndpoint(api.Endpoint):
    model = Dataset
    base_serializer = serializers.HyperlinkedModelSerializer
    url = "datasets"
    exclude_fields = [
        "project",
    ]


@api.register
class SampleEndpoint(api.Endpoint):
    model = Sample
    exclude_fields = ["dataset", "geom"]
    url = "samples"


@api.register
class SiteEndpoint(api.Endpoint):
    model = Site
    url = "sites"
    exclude_fields = ["dataset"]
