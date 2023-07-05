from django.urls import include, path

from geoluminate.views import placeholder_view

from .views import dataset, project, sample

urlpatterns = [
    path("projects/", project.ProjectDataTable.as_view(), name="project_list"),
    path(
        "projects/add/",
        project.ProjectEditView.as_view(extra_context={"add": True}),
        name="project-add",
    ),
    path(
        "projects/<int:pk>/edit/",
        project.ProjectEditView.as_view(extra_context={"add": False}),
        name="project-edit",
    ),
    path("projects/<int:pk>/", project.ProjectDetailView.as_view(), name="project_detail"),
    path("datasets/", dataset.DatasetDataTable.as_view(), name="dataset_list"),
    path("datasets/<int:pk>/", dataset.DatasetDetailView.as_view(), name="dataset_detail"),
    path("samples/", sample.SampleDataTable.as_view(), name="sample_list"),
    path("samples/<int:pk>/", sample.SampleDetailView.as_view(), name="sample_detail"),
]
