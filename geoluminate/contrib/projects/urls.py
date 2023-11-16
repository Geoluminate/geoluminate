from django.urls import include, path

from geoluminate.plugins import project

from .views import AddProjectView, ProjectListView

app_name = "projects"
urlpatterns = [
    path("projects/new/", AddProjectView.as_view(), name="add"),
    path("projects/", ProjectListView.as_view(), name="list"),
    path("p/<uuid:uuid>/", include(project.urls)),
]
