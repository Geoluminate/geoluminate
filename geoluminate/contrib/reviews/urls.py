from django.urls import path

from .views import (
    LiteratureReviewListView,
    ReviewCreateView,
    ReviewListView,
    ReviewLiteratureEdit,
)

app_name = "reviews"
urlpatterns = [
    path("reviews/start/", ReviewCreateView.as_view(), name="add"),
    # path("reviews/", ReviewListView.as_view(), name="list"),
    path("reviews/<pk>/", ReviewLiteratureEdit.as_view(), name="edit"),
    path("reviews/", LiteratureReviewListView.as_view(), name="list"),
]
