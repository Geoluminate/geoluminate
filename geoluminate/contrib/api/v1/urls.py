from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView
from rest_framework_nested import routers

# from views import DomainViewSet, NameserverViewSet
from geoluminate.api import API

from ...controlled_vocabulary.api.viewsets import ControlledVocabularyViewSet

# from geoluminate.contrib.project.api.urls import urlpatterns as project_urls
router = routers.SimpleRouter()
router.register(r"vocabularies", ControlledVocabularyViewSet)

# domains_router = routers.NestedSimpleRouter(router, r"domains", lookup="domain")
# domains_router.register(r"nameservers", NameserverViewSet, basename="domain-nameservers")

urlpatterns = [
    path("", include("geoluminate.contrib.project.api.urls")),
    path("", include("geoluminate.contrib.user.api.urls")),
    # path("", include("geoluminate.contrib.controlled_vocabulary.api.urls")),
    path("measurements/", include(API.urls)),
    path("", include(router.urls)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # path("auth/", include("rest_framework.urls", namespace="rest_framework")),
]
