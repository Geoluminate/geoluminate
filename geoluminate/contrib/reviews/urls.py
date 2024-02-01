from django.urls import path
from django.views.generic import DetailView

from .models import Review
from .views import (
    AcceptLiteratureReview,
    LiteratureReviewListView,
    ReviewLiteratureEdit,
    accept_review,
    reject_review,
    submit_review,
)

app_name = "review"
urlpatterns = [
    path("literature/<pk>/accept/", AcceptLiteratureReview.as_view(), name="accept-literature"),
    path("reviews/<pk>/", DetailView.as_view(model=Review), name="edit"),
    path("reviews/<pk>/accept/", accept_review, name="accept"),
    path("reviews/<pk>/submit/", submit_review, name="submit"),
    path("reviews/<pk>/reject/", reject_review, name="reject"),
    path("reviews/<pk>/delete/", reject_review, name="delete"),
    path("reviews/", LiteratureReviewListView.as_view(), name="list"),
]
