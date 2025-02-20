from django.urls import include, path
from rest_framework_nested import routers

from .viewsets import (
    ContributorViewset,
)

router = routers.SimpleRouter()
router.register(r"contributors", ContributorViewset)

contributor_router = routers.NestedSimpleRouter(router, r"contributors", lookup="contributor")
# contributor_router.register(r"projects", ContributorProjectViewset, basename="contributor-projects")
# contributor_router.register(r"datasets", ContributorDatasetViewset, basename="contributor-datasets")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(contributor_router.urls)),
]
