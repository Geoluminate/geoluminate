import json

from django.contrib.gis.measure import Distance
from django.db.models import F
from rest_framework_gis import filters

# from rest_framework_gis.filters import DistanceToPointFilter
# from geoluminate.contrib.samples.serializers import SampleGeojsonSerializer
from .models import Location


def serialize_dataset_samples(self, dataset):
    qs = dataset.samples.annotate(geom=F("location__point"))  # noqa: F841
    # serializer = SampleGeojsonSerializer(qs, many=True)
    # return {str(dataset.pk): json.dumps(serializer.data)}
    return {str(dataset.pk): json.dumps([])}


def get_sites_within(location, radius=25):
    """Gets nearby sites within {radius} km radius"""
    qs = Location.obejcts.filter(point__distance_lt=(location.point, Distance(km=radius)))  # noqa: F841


class DistanceToPointOrderingFilter(filters.DistanceToPointOrderingFilter):
    def get_schema_operation_parameters(self, view):
        params = super().get_schema_operation_parameters(view)
        params.append(
            {
                "name": self.order_param,
                "required": False,
                "in": "query",
                "description": "",
                "schema": {
                    "type": "enum",
                    "items": {"type": "string", "enum": ["asc", "desc"]},
                    "example": "desc",
                },
                "style": "form",
                "explode": False,
            }
        )
        return params
