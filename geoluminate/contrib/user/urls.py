from django.urls import path

from . import views

app_name = "user"
urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("settings/", views.Account.as_view(), name="account"),
    path("profile/<pk>/", views.profile, name="profile"),
    path("orcid/", views.orcid, name="why_orcid"),
    path("community/", views.community, name="community"),
]
