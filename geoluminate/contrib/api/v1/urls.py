from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView

from geoluminate.api import API

urlpatterns = [
    path("", include(API.urls)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("auth/", include("rest_framework.urls", namespace="rest_framework")),
]
