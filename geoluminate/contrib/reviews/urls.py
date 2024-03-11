from django.urls import include, path
from django.views.generic import DetailView

from geoluminate.contrib.datasets.plugins import dataset

from .models import Review
from .views import (
    AcceptLiteratureReview,
    AddLiteratureView,
    LiteratureListView,
    LiteratureReviewListView,
    reject_review,
    submit_review,
)

app_name = "review"
urlpatterns = [
    path(
        "literature/",
        include(
            [
                path("new/", AddLiteratureView.as_view(), name="literature_create"),
                path("", LiteratureListView.as_view(), name="literature_list"),
                path("<pk>/accept/", AcceptLiteratureReview.as_view(), name="accept-literature"),
            ]
        ),
    ),
    path(
        "review/",
        include(
            [
                path("", LiteratureReviewListView.as_view(), name="list"),
                path("<uuid:uuid>/", include(dataset.urls)),
                path("<pk>/", DetailView.as_view(model=Review), name="edit"),
                # path("<pk>/accept/", accept_review, name="accept"),
                path("<pk>/submit/", submit_review, name="submit"),
                path("<pk>/reject/", reject_review, name="reject"),
                path("<pk>/delete/", reject_review, name="delete"),
            ]
        ),
    ),
]
