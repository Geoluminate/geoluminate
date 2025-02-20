from django.urls import include, path

from .views import ContributorContactView
from .views.contribution import AddContributionView
from .views.edit import UpdateAffiliations, UpdateIdentifiers, UpdateProfile
from .views.organization import OrganizationCreateView, OrganizationListView, OrgRORCreateView
from .views.person import ContributorCRUDView

# personal = [*PersonCRUDView.get_urls()]

account = [
    path("profile/", UpdateProfile.as_view(), name="contributor-profile"),
    path("identifiers/", UpdateIdentifiers.as_view(), name="contributor-identifiers"),
    path("affiliations/", UpdateAffiliations.as_view(), name="contributor-affiliations"),
]


urlpatterns = [
    path("account/", include(account)),
    *ContributorCRUDView.get_urls(),
    # path("", include(personal)),
    path("contributor/<str:pk>/contact/", ContributorContactView.as_view(), name="contributor-contact"),
    path("organization/add/", OrganizationCreateView.as_view(), name="create"),
    path("organization/list/", OrganizationListView.as_view(), name="list"),
    path("organization/add/ror/", OrgRORCreateView.as_view(), name="ror-create"),
    path("contribution/add/<str:base_pk>", AddContributionView.as_view(), name="contribution-create"),
]
