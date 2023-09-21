from django.urls import include, path
from django.views.generic import TemplateView

# from .views.account import AccountEmailView
from .views.users import (
    Account,
    AffiliationView,
    Dashboard,
    ProfileView,
    Reviews,
    user_datasets_view,
    user_projects_view,
)

urlpatterns = [
    # path("account/email/", AccountEmailView.as_view(), name="account_email"),
    path("", include("allauth.urls")),
    path(
        "",
        include(
            (
                [
                    path("dashboard/", Dashboard.as_view(), name="dashboard"),
                    path("reviews/", Reviews.as_view(), name="reviews"),
                    path("settings/", Account.as_view(), name="account"),
                    path("projects/", user_projects_view, name="projects"),
                    path("datasets/", user_datasets_view, name="datasets"),
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
