from django.urls import path

from .views import OrganizationCreateView, OrganizationListView

app_name = "organizations"
urlpatterns = [
    path("organization/add/", OrganizationCreateView.as_view(), name="create"),
    path("organization/list/", OrganizationListView.as_view(), name="list"),
]
