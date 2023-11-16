from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView
from literature.api.urls import router as lit_router
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
nested_dataset.register(r"samples", viewsets.NestedSamples, basename="samples")

# ============= NESTED SAMPLE ROUTER =============
nested_samples = routers.NestedSimpleRouter(router, r"samples", lookup="sample")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(nested_project.urls)),
    path("", include(nested_dataset.urls)),
    path("", include(nested_samples.urls)),
    path("measurements/", MeasurementMetadataView.as_view(), name="measurement-metadata"),
    path("measurements/", include(measurements.router.urls)),
    path("literature/", include(lit_router.urls)),
    path("", include("geoluminate.contrib.users.api.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # path("auth/", include("rest_framework.urls", namespace="rest_framework")),
]

# print(measurements.registry)
# for p in measurements.router.urls:
#     print(p)


# In django rest framework, I am using a hyperlinkedmodelserializer on a model that contains a uuid field. I have set my lookup_field on my viewset as "uuid" but the hyperlinkedmodelserializer does not use that lookup correctly. How can I tell the hyperlinkedmodelserializer to resolve urls using the uuid field?
