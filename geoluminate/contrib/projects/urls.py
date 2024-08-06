from django.urls import include, path
from neapolitan.views import Role

from geoluminate.contrib.datasets.views import DatasetEditView

from .plugins import project
from .views import ProjectEditView, ProjectListView

urlpatterns = [
    *ProjectEditView.get_urls(),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path("p/<uuid:pk>/", include(project.urls)),
    path("p/<uuid:pk>/", include(DatasetEditView.get_urls(roles=[Role.CREATE]))),
]
