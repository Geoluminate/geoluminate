from django.urls import include, path
from django.views.generic import TemplateView

# from .views.account import AccountEmailView
from .views import ContributorDetailView, ContributorListView

app_name = "contributor"
urlpatterns = [
    path("", ContributorListView.as_view(), name="list"),
    path("<pk>/", ContributorDetailView.as_view(), name="detail"),
]
