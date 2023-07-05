# from django.shortcuts import redirect
from django.urls import include, path
from drf_spectacular.views import SpectacularSwaggerView

# app_name = "api"
urlpatterns = [
    path(
        "",
        SpectacularSwaggerView.as_view(template_name="geoluminate/spectacular.html", url_name="schema"),
        name="swagger-ui",
    ),
    path("v1/", include("geoluminate.contrib.api.v1.urls")),
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/register/", include("dj_rest_auth.registration.urls")),
    # path("", lambda request: redirect("swagger-ui", permanent=False)),
    # path("", lambda request: redirect("/api/v1", permanent=True)),
]
