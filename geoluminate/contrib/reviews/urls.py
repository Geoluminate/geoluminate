from django.urls import include, path
from django.views.generic import DetailView

# from geoluminate.contrib.datasets.plugins import dataset
from .models import Review
from .views import (
    AcceptLiteratureReview,
    LiteratureEditView,
    LiteratureListView,
    LiteratureReviewListView,
    reject_review,
    submit_review,
)

# app_name = "review"
urlpatterns = [
    path(
        "literature/",
        include(
            [
                path("", LiteratureListView.as_view(), name="literature-list"),
                *LiteratureEditView.get_urls(),
                path(
                    "<pk>/accept/",
                    AcceptLiteratureReview.as_view(),
                    name="literature-accept",
                ),
            ]
        ),
    ),
    path(
        "review/",
        include(
            [
                path("", LiteratureReviewListView.as_view(), name="review-list"),
                # path("<uuid:pk>/", include(dataset.urls)),
                path("<pk>/", DetailView.as_view(model=Review), name="review-edit"),
                path("<pk>/submit/", submit_review, name="review-submit"),
                path("<pk>/reject/", reject_review, name="review-reject"),
                path("<pk>/delete/", reject_review, name="review-delete"),
            ]
        ),
    ),
]
