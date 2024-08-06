from django.urls import include, path

from .views import AccountEdit, CodeOfConduct, TermsOfUse

app_name = "user"
urlpatterns = [
    path(
        "general/",
        include(
            [
                path("appearance/", AccountEdit.as_view(), name="appearance-settings"),
                path("notifications/", AccountEdit.as_view(), name="notifications-settings"),
                path("privacy/", AccountEdit.as_view(), name="notifications-settings"),
            ]
        ),
    ),
    path(
        "agreements/",
        include(
            [
                path("code-of-conduct/", CodeOfConduct.as_view(), name="code_of_conduct"),
                path("terms-of-use/", TermsOfUse.as_view(), name="terms"),
            ]
        ),
    ),
]
