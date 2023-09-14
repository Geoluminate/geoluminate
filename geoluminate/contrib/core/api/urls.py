from django.urls import include, path
from literature.api.views import LiteratureViewSet
from rest_framework_nested import routers

# from geoluminate.contrib.literature.api.views import LiteratureViewSet
from geoluminate.contrib.core import api

# ============= BASE ROUTERS =============
router = routers.SimpleRouter()
router.register(r"projects", api.ProjectViewset)
router.register(r"datasets", api.DatasetViewset)
router.register(r"samples", api.SampleViewset)
router.register(r"locations", api.SiteViewset)
router.register(r"literature", LiteratureViewSet)

# ============= NESTED PROJECT ROUTER =============
project_router = routers.NestedSimpleRouter(router, r"projects", lookup="project")
project_router.register(r"datasets", api.DatasetViewset)

# ============= NESTED DATASET ROUTER =============
dataset_router = routers.NestedSimpleRouter(router, r"datasets", lookup="dataset")
dataset_router.register(r"samples", api.SampleViewset)
dataset_router.register(r"locations", api.SiteViewset)


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


urlpatterns = [
    path("", include(router.urls)),
    path("", include(project_router.urls)),
    path("", include(dataset_router.urls)),
    path("", include(location_router.urls)),
    path("", include(sample_router.urls)),
]
