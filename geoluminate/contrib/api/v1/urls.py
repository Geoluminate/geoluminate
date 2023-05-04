from django.urls import include, path
from drf_auto_endpoint.router import router
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from geoluminate.contrib.api.v1 import views
from geoluminate.utils import get_database_models

for model in get_database_models():
    router.register(model)

drf_router = DefaultRouter()
drf_router.register("sites", views.SiteViewSet, basename="sites")

urlpatterns = [
    path(
        "",
        SpectacularSwaggerView.as_view(template_name="geoluminate/spectacular.html", url_name="schema"),
        name="swagger-ui",
    ),
    path("", include(router.urls)),
    path("", include(drf_router.urls)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("auth/", include("rest_framework.urls", namespace="rest_framework")),
]

# urlpatterns.extend(urls)
