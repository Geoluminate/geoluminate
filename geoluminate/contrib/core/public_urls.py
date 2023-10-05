from django.urls import include, path

from geoluminate.contrib.datasets.models import Dataset
from geoluminate.contrib.datasets.views import DatasetDetail
from geoluminate.contrib.projects.models import Project
from geoluminate.contrib.projects.views import ProjectDetail
from geoluminate.contrib.samples.views import SampleDetail
from geoluminate.contrib.samples.views import list_view as sample_list_view

from .views import list_view

app_name = "core"
urlpatterns = [
    path("projects/", list_view(model=Project), name="project-list"),
    path("projects/<uuid:uuid>/", ProjectDetail.as_view(app_name="core")),
    path("datasets/", list_view(model=Dataset), name="dataset_list"),
    path("datasets/<uuid:uuid>/", DatasetDetail.as_view(app_name="core"), name="dataset-detail"),
    path("samples/", sample_list_view, name="sample_list"),
    path("samples/<uuid:uuid>/", SampleDetail.as_view(), name="sample_detail"),
    path("measurements/", sample_list_view, name="measurement_list"),
]
