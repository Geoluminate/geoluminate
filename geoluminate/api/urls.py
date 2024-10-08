# from django.shortcuts import redirect
from django.urls import include, path
from drf_spectacular.views import SpectacularSwaggerView

from .views import TOSView

app_name = "api"
urlpatterns = [
    path(
        "",
        SpectacularSwaggerView.as_view(template_name="geoluminate/generic/spectacular.html", url_name="api:schema"),
        name="swagger-ui",
    ),
    path("v1/", include("geoluminate.api.v1.urls")),
    path("v1/tos/", TOSView.as_view(), name="tos"),
    # path("auth/", include("dj_rest_auth.urls")),
    # path("auth/register/", include("dj_rest_auth.registration.urls")),
    # path("", lambda request: redirect("swagger-ui", permanent=False)),
    # path("", lambda request: redirect("/api/v1", permanent=True)),
]
