from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView

# from views import DomainViewSet, NameserverViewSet
# from geoluminate.api import API

urlpatterns = [
    path("", include("geoluminate.contrib.core.api.urls")),
    path("", include("geoluminate.contrib.user.api.urls")),
    # path("measurements/", include(API.urls)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # path("auth/", include("rest_framework.urls", namespace="rest_framework")),
]
