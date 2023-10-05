from django.urls import include, path

# from .views import dataset, project, review, sample
from .views import create_view

urlpatterns = [
    # path("projects/<uuid:uuid>/", projects.ProjectDetail.as_view(extra_context={"edit": True}, name="project-edit")),
    path("", include("geoluminate.contrib.datasets.urls")),
    # path("datasets/<uuid:uuid>/descriptions/", dataset.EditDescription.as_view(), name="dataset-description-edit"),
    # path("datasets/<uuid:uuid>/", datasets.DatasetEdit.as_view(name="dataset-edit", extra_context={"edit": True})),
    # path("datasets/<uuid:uuid>/descriptions/add/", dataset.AddDescription.as_view(), name="dataset-description-add"),
    # path("samples/<uuid:uuid>/", datasets.DatasetDetail.as_view(extra_context={"edit": True}, name="sample-edit")),
    # path(
    #     "new/",
    #     include(
    #         [
    #             path("project/", project.AddProjectView.as_view(), name="project-add"),
    #             path("review/", review.AddReviewView.as_view(), name="review-add"),
    #             # path("project/", create_view(form_class=ProjectFormCollection), name="project-add"),
    #             path("dataset/", dataset.AddDatasetView.as_view(), name="dataset-add"),
    #             # path("dataset/", create_view(model=Dataset, fields=["project", "title"]), name="dataset-add"),
    #             path("sample/", create_view(model=Sample, fields=["dataset", "title"]), name="sample-add"),
    #             path("description/", create_view(form_class=GenericDescriptionForm), name="description-add"),
    #         ]
    #     ),
    # ),
]
