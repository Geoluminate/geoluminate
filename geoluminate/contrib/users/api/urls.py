from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView
from rest_framework_nested import routers

from .viewsets import (
    ContributorDatasetViewset,
    ContributorProjectViewset,
    ProfileViewset,
)

router = routers.SimpleRouter()
router.register(r"contributors", ProfileViewset)

contributor_router = routers.NestedSimpleRouter(router, r"contributors", lookup="contributor")
# contributor_router.register(r"projects", ContributorProjectViewset, basename="contributor-projects")
# contributor_router.register(r"datasets", ContributorDatasetViewset, basename="contributor-datasets")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(contributor_router.urls)),
]
