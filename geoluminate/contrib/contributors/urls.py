from django.urls import include, path
from django.views.generic import RedirectView

from .plugins import contributor
from .views import ContributorContactView, ContributorListView
from .views.edit import UpdateAffiliations, UpdateIdentifiers, UpdateProfile

urlpatterns = [
    path(
        "profile/",
        include(
            [
                path(
                    "",
                    RedirectView.as_view(pattern_name="contributor-profile", permanent=True),
                    name="profile-redirect",
                ),
                path("public/", UpdateProfile.as_view(), name="contributor-profile"),
                path("identifiers/", UpdateIdentifiers.as_view(), name="contributor-identifiers"),
                path("affiliations/", UpdateAffiliations.as_view(), name="contributor-affiliations"),
            ]
        ),
    ),
    path("contributors/", ContributorListView.as_view(), name="contributor-list"),
    path("c/<uuid:pk>/", include(contributor.urls)),
    path("c/<uuid:pk>/contact/", ContributorContactView.as_view(), name="contributor-contact"),
    # path(
    #     "<str:model>/<uuid:pk>/",
    #     include(ContributionCRUDView.get_urls(roles=[Role.CREATE, Role.UPDATE, Role.DELETE])),
    # ),
    # path("<str:otype>/<uuid:object_pk>/", include(ContributionCRUDView.as_urls(roles=[Role.CREATE, Role.UPDATE, Role.DELETE]))),
]
