from rest_framework.fields import Field as Field
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from geoluminate.api.serializers import BaseSerializerMixin

from .models import Project


class ProjectSerializer(BaseSerializerMixin, NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        "project_uuid": "project__uuid",
    }

    # datasets = NestedHyperlinkedIdentityField(
    #     view_name="dataset-list",
    #     lookup_field="uuid",
    #     lookup_url_kwarg="project_uuid",
    # )

    class Meta:
        model = Project
        exclude = ["options", "visibility"]
        # extra_kwargs = {
        #     "details": {"lookup_field": "uuid"},
        #     "project": {"lookup_field": "uuid"},
        #     "dataset": {"lookup_field": "uuid"},
        #     "sample": {"lookup_field": "uuid"},
        #     "parent": {"lookup_field": "uuid"},
        #     "location": {"lookup_field": "uuid"},
        # }
