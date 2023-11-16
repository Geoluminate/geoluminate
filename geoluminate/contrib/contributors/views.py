from geoluminate.views import BaseDetailView, BaseListView

from .filters import ContributionFilter, ContributorFilter
from .models import Contribution, Contributor


class ContributorListView(BaseListView):
    model = Contributor
    filterset_class = ContributorFilter


class ContributorDetailView(BaseDetailView):
    model = Contributor
    list_object = None

    def has_edit_permission(self):
        """Returns True if the user has permission to edit the profile. This is determined by whether the profile belongs to the current user."""
        return self.request.user.profile == self.get_object()


class ContributionListView(BaseListView):
    model = Contribution
    filterset_class = ContributionFilter
