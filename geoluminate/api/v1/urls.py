from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView
from literature.api.views import LiteratureViewSet
from rest_framework_nested import routers

# from geoluminate.contrib.literature.api.views import LiteratureViewSet
from .. import viewsets

# ============= BASE ROUTERS =============
router = routers.SimpleRouter()
router.register(r"projects", viewsets.ProjectViewset)
router.register(r"datasets", viewsets.DatasetViewset)
router.register(r"samples", viewsets.SampleViewset)
router.register(r"locations", viewsets.SiteViewset)
router.register(r"literature", LiteratureViewSet)

# ============= NESTED PROJECT ROUTER =============
project_router = routers.NestedSimpleRouter(router, r"projects", lookup="project")
project_router.register(r"datasets", viewsets.DatasetViewset)

# ============= NESTED DATASET ROUTER =============
dataset_router = routers.NestedSimpleRouter(router, r"datasets", lookup="dataset")
dataset_router.register(r"samples", viewsets.SampleViewset)
dataset_router.register(r"locations", viewsets.SiteViewset)


# ============= NESTED SITE ROUTER =============
location_router = routers.NestedSimpleRouter(router, r"locations", lookup="location")
# location_router.register(r"samples", api.SampleViewset)

# ============= NESTED SAMPLE ROUTER =============
sample_router = routers.NestedSimpleRouter(router, r"samples", lookup="sample")


# ============= MEASUREMENT ROUTER =============
# router.register(r"measurements", SampleViewset, basename="measurement)


# for measurement_type in get_measurement_types():
#     viewset = viewset_factory(measurement_type.model)
#     measurement_router.register(
#         measurement_type.name, SampleViewset, basename=measurement_type.name
#     )

# from views import DomainViewSet, NameserverViewSet
# from geoluminate.api import API

urlpatterns = [
    path("", include(router.urls)),
    path("", include(project_router.urls)),
    path("", include(dataset_router.urls)),
    path("", include(location_router.urls)),
    path("", include(sample_router.urls)),
    path("", include("geoluminate.contrib.users.api.urls")),
    # path("measurements/", include(API.urls)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # path("auth/", include("rest_framework.urls", namespace="rest_framework")),
]
