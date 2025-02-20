# import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, ListView
from meta.views import MetadataMixin

from ..forms.organization import RORForm
from ..models import Organization


class OrganizationListView(MetadataMixin, LoginRequiredMixin, ListView):
    """List of organizations that the user is a member of."""

    model = Organization

    def get_queryset(self):
        return self.org_model.active.filter(users=self.request.user)


class OrgRORCreateView(MetadataMixin, LoginRequiredMixin, CreateView):
    """Create a new organization using the RORForm."""

    model = Organization
    template_name = "organizations/organization_form.html"
    success_url = "/"
    form_class = RORForm

    def get_success_url(self):
        return reverse("organization-detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        data = form.cleaned_data["data"]
        # if data["orcid-identifier"]:
        #     c = contributor_from_orcid(data)
        # elif data["id"].startswith("https://ror.org/"):
        #     c = contributor_from_ror(data)
        # # Organization.from_ror(form.cleaned_data["data"])
        # return HttpResponseRedirect(self.get_success_url())
        # return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class OrganizationCreateView(MetadataMixin, LoginRequiredMixin, CreateView):
    """Create a new organization."""

    template_name = "organizations/organization_form.html"
    success_url = "/"
    form_class = RORForm


class OrganizationUserListView(MetadataMixin, ListView):
    """List of users in an organization."""

    org_model = Organization

    def get(self, request, *args, **kwargs):
        self.organization = self.get_organization()
        self.object_list = self.organization.organization_users.all()
        context = self.get_context_data(
            object_list=self.object_list,
            organization_users=self.object_list,
            organization=self.organization,
        )
        return self.render_to_response(context)
