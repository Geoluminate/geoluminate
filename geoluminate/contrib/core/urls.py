from django.urls import include, path

from .views import dataset, project, sample

# app_name = "core"
urlpatterns = [
    path(
        "projects/",
        include(
            [
                path("<uuid:uuid>/", project.edit_view, name="project-edit"),
            ],
        ),
    ),
    path(
        "datasets/",
        include(
            [
                path("<uuid:uuid>/", dataset.edit_view, name="dataset-edit"),
            ]
        ),
    ),
    # path(
    #     "samples/", include([
    #         path("add/", views.SampleEdit.as_view(extra_context={"add": True}), name="sample-add"),
    #         path("<uuid:uuid>/edit/", views.SampleEdit.as_view(extra_context={"add": False}), name="sample-edit"),
    #     ])
    # ),
    path(
        "new/",
        include(
            [
                path("project/", project.add_view, name="project-add"),
                path("dataset/", dataset.add_view, name="dataset-add"),
                # path("sample/", sample.add_view, name="sample-add"),
            ]
        ),
    ),
]
