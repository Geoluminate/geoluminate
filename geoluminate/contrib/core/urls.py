from django.urls import include, path

from .views import dataset, project, sample

urlpatterns = [
    path(
        "projects/",
        include(
            [
                path("add/", project.add_view, name="project-add"),
                path("<uuid:uuid>/", project.edit_view, name="project-edit"),
            ],
        ),
    ),
    path(
        "datasets/",
        include(
            [
                path("add/", dataset.add_view, name="dataset-add"),
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
]
