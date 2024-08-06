# import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.views.generic import CreateView, ListView

from geoluminate.views import BaseMixin

from .forms import OrganizationCreateForm
from .models import Organization


class OrganizationMixin:
    """Mixin used like a SingleObjectMixin to fetch an organization"""

    org_model = Organization
    org_context_name = "organization"

    def get_org_model(self):
        return self.org_model

    def get_context_data(self, **kwargs):
        kwargs.update({self.org_context_name: self.organization})
        return super().get_context_data(**kwargs)

    @cached_property
    def organization(self):
        organization_pk = self.kwargs.get("organization_pk", None)
        return get_object_or_404(self.get_org_model(), pk=organization_pk)

    def get_object(self):
        return self.organization

    get_organization = get_object  # Now available when `get_object` is overridden


class OrganizationListView(BaseMixin, LoginRequiredMixin, OrganizationMixin, ListView):
    """List of organizations that the user is a member of."""

    model = Organization

    def get_queryset(self):
        return self.org_model.active.filter(users=self.request.user)


class OrganizationCreateView(BaseMixin, LoginRequiredMixin, CreateView):
    """Create a new organization."""

    template_name = "organizations/organization_form.html"
    success_url = "/"
    form_class = OrganizationCreateForm

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({"request": self.request})
    #     return kwargs


class OrganizationUserListView(BaseMixin, OrganizationMixin, ListView):
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
