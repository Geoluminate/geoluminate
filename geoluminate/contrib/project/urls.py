from django.urls import include, path

from . import views

urlpatterns = [
    path(
        "projects/",
        include(
            [
                path(
                    "add/",
                    views.ProjectEdit.as_view(extra_context={"add": True}),
                    name="project-add",
                ),
                path(
                    "<uuid:uuid>/",
                    views.ProjectEdit.as_view(extra_context={"edit": True}),
                    name="project-edit",
                ),
            ],
        ),
    ),
    path(
        "datasets/",
        include(
            [
                path("add/", views.DatasetEdit.as_view(extra_context={"add": True}), name="dataset-add"),
                path("<uuid:uuid>/", views.DatasetEdit.as_view(extra_context={"add": False}), name="dataset-edit"),
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
