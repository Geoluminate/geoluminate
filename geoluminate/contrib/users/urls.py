from django.urls import include, path
from django.views.generic import TemplateView

# from .views.account import AccountEmailView
from .views import Account, AffiliationView, ProfileRedirectView

urlpatterns = [
    # path("account/email/", AccountEmailView.as_view(), name="account_email"),
    path("", include("allauth.urls")),
    path(
        "",
        include(
            (
                [
                    path("profile/", ProfileRedirectView.as_view(), name="profile"),
                    path("settings/", Account.as_view(), name="account"),
                    path("affiliations/", AffiliationView.as_view(), name="affiliations"),
                ],
                "user",
            ),
        ),
        {"base_template": "user/base_list.html", "can_create": True},
    ),
    path(
        "code-of-conduct/",
        TemplateView.as_view(template_name="geoluminate/generic/code_of_conduct.html"),
        name="code_of_conduct",
    ),
]
