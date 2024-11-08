from django.urls import include, path

from geoluminate.plugins import plugins

from .views import ProjectCRUDView

urlpatterns = [
    *ProjectCRUDView.get_urls(),
    path("project/<str:pk>/", include(plugins.get_urls("project"))),
]
