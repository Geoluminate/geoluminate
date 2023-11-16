from django.urls import include, path

from geoluminate.plugins import contributor

from .views import ContributorListView

app_name = "contributor"
urlpatterns = [
    path("contributors/", ContributorListView.as_view(), name="list"),
    path("c/<uuid:uuid>/", include(contributor.urls)),
]
