from django.db.models.base import Model as Model
from django.utils.translation import gettext as _

from geoluminate.views import BaseDetailView, BaseFormView, BaseListView

from .filters import ContributionFilter, ContributorFilter
from .forms import ContributionForm, UserProfileForm
from .models import Contribution, Contributor


class ContributorListView(BaseListView):
    model = Contributor
    filterset_class = ContributorFilter


class ContributorDetailView(BaseDetailView):
    model = Contributor
    list_object = None
    allow_discussion = False

    def has_edit_permission(self):
        """Returns True if the user has permission to edit the profile. This is determined by whether the profile belongs to the current user."""

        # check if current user is logged in
        if self.request.user.is_anonymous:
            return False

        return self.request.user.profile == self.get_object()


class ContributorFormView(BaseFormView):
    model = Contributor
    form_class = UserProfileForm
    template_name = "contributors/contributor_form.html"
    success_url = "."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context["editing"] = True

        return context


# CONTRIBUTION VIEWS
class ContributionListView(BaseListView):
    model = Contribution
    filterset_class = ContributionFilter
    columns = 3


class ContributionEditView(BaseFormView):
    model = Contribution
    form_class = ContributionForm
    title = _("Add contributor")

    def get_object(self, queryset):
        obj = super().get_object(queryset)
        contributor = obj.contributions.get(uuid=self.kwargs.get("contribution"))
        return contributor
