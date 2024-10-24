from django.urls import include, path

from .plugins import contributor
from .views import ContributorContactView, ContributorListView
from .views.edit import UpdateAffiliations, UpdateIdentifiers, UpdateProfile
from .views.organization import OrganizationCreateView, OrganizationListView

urlpatterns = [
    path(
        "account/",
        include(
            [
                path("profile/", UpdateProfile.as_view(), name="contributor-profile"),
                path("identifiers/", UpdateIdentifiers.as_view(), name="contributor-identifiers"),
                path("affiliations/", UpdateAffiliations.as_view(), name="contributor-affiliations"),
            ]
        ),
    ),
    path("contributors/", ContributorListView.as_view(), name="contributor-list"),
    path("c/<str:pk>/", include(contributor.urls)),
    path("c/<str:pk>/contact/", ContributorContactView.as_view(), name="contributor-contact"),
    path("organization/add/", OrganizationCreateView.as_view(), name="create"),
    path("organization/list/", OrganizationListView.as_view(), name="list"),
    # path(
    #     "<str:model>/<str:pk>/",
    #     include(ContributionCRUDView.get_urls(roles=[Role.CREATE, Role.UPDATE, Role.DELETE])),
    # ),
    # path("<str:otype>/<uuid:object_pk>/", include(ContributionCRUDView.as_urls(roles=[Role.CREATE, Role.UPDATE, Role.DELETE]))),
]
