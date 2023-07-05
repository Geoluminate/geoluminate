from django.urls import path

from geoluminate.views import placeholder_view

from . import views

app_name = "user"
urlpatterns = [
    path("community/", placeholder_view, name="community_members"),
    path("community/directory/", views.CommunityDirectoryView.as_view(), name="member_directory"),
    path("dashboard/", placeholder_view, name="dashboard"),
    path("settings/", views.Account.as_view(), name="account"),
    path(
        "profile/",
        views.ProfileView.as_view(extra_context={"add": False}),
        name="profile-edit",
    ),
    path(
        "projects/",
        views.UserProjectListView.as_view(),
        name="projects",
    ),
]
