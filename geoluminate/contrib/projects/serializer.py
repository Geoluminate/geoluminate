from rest_framework.fields import Field as Field
from rest_framework.serializers import HyperlinkedIdentityField, ModelSerializer

from .models import Project


class ProjectSerializer(ModelSerializer):
    web = HyperlinkedIdentityField(view_name="project-detail")
    # dates = DateSerializer(many=True)

    class Meta:
        model = Project
        exclude = ["visibility", "options"]
        expandable_fields = {
            "datasets": (
                "geoluminate.api.serializers.DatasetSerializer",
                {"many": True},
            )
        }
