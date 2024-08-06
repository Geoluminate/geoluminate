from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView
from rest_framework_nested import routers

from geoluminate.measurements import measurements

from ..views import MeasurementMetadataView
from . import viewsets

# ============= BASE ROUTERS =============
router = routers.SimpleRouter()
router.register(r"projects", viewsets.ProjectViewset)
router.register(r"datasets", viewsets.DatasetViewset)
router.register(r"samples", viewsets.SampleViewset)

# ============= NESTED PROJECT ROUTER =============
nested_project = routers.NestedSimpleRouter(router, r"projects", lookup="project")
nested_project.register(r"datasets", viewsets.NestedDatasets)
nested_project.register(r"samples", viewsets.NestedSamples)

# ============= NESTED DATASET ROUTER =============
nested_dataset = routers.NestedSimpleRouter(router, r"datasets", lookup="dataset")
nested_dataset.register(r"samples", viewsets.NestedSamples)

# ============= NESTED SAMPLE ROUTER =============
nested_samples = routers.NestedSimpleRouter(router, r"samples", lookup="sample")

app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
    path("", include(nested_project.urls)),
    path("", include(nested_dataset.urls)),
    path("", include(nested_samples.urls)),
    path("measurements/", MeasurementMetadataView.as_view(), name="measurement-metadata"),
    path("measurements/", include(measurements.router.urls)),
    path("", include("geoluminate.contrib.users.api.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # path("auth/", include("rest_framework.urls", namespace="rest_framework")),
]
