from django.shortcuts import redirect
from django.urls import include, path

# app_name = 'api'
urlpatterns = [
    path("v1/", include("geoluminate.contrib.api.v1.urls")),
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/register/", include("dj_rest_auth.registration.urls")),
    path("", lambda request: redirect("/api/v1", permanent=True)),
]
