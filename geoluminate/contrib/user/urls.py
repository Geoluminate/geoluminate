from django.urls import include, path
from django.views.generic import TemplateView

from geoluminate.views import placeholder_view

# from .views.account import AccountEmailView
from .views.community import CommunityDirectoryView, MemberProfileView
from .views.users import (
    Account,
    AffiliationView,
    Dashboard,
    ProfileView,
    Reviews,
    UserDatasets,
    UserProjects,
)

urlpatterns = [
    # path("account/email/", AccountEmailView.as_view(), name="account_email"),
    path(
        "community/",
        include(
            (
                [
                    path("", placeholder_view, name="members"),
                    path("members/", CommunityDirectoryView.as_view(), name="directory"),
                    path("members/<pk>/", MemberProfileView.as_view(), name="profile"),
                ],
                "community",
            ),
        ),
    ),
    path("", include("allauth.urls")),
    path(
        "",
        include(
            (
                [
                    path("dashboard/", Dashboard.as_view(), name="dashboard"),
                    path("reviews/", Reviews.as_view(), name="reviews"),
                    path("settings/", Account.as_view(), name="account"),
                    path("projects/", UserProjects.as_view(), name="projects"),
                    path("datasets/", UserDatasets.as_view(), name="datasets"),
                    # path("samples/", UserProjects.as_view(), name="projects"),
                    path(
                        "profile/",
                        ProfileView.as_view(extra_context={"add": False}),
                        name="profile_edit",
                    ),
                    path("affiliations/", AffiliationView.as_view(), name="affiliations"),
                ],
                "user",
            ),
        ),
    ),
    path(
        "code-of-conduct/",
        TemplateView.as_view(template_name="geoluminate/generic/code_of_conduct.html"),
        name="code_of_conduct",
    ),
]
