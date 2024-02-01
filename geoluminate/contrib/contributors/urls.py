from django.urls import include, path

from geoluminate.plugins import contributor

from .views import ContributionEditView, ContributorFormView, ContributorListView

app_name = "contributor"
urlpatterns = [
    path("contributors/", ContributorListView.as_view(), name="list"),
    path("c/<uuid:uuid>/", include(contributor.urls)),
    path("c/<uuid:uuid>/edit/", ContributorFormView.as_view(), name="edit"),
]

contribution_patterns = [
    path("contributor/<uuid:contributor>/", ContributionEditView.as_view(), name="edit"),
    path("contributor/add/", ContributionEditView.as_view(extra_context={"add": True}), name="add"),
]
