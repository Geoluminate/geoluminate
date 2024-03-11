# import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.views.generic import ListView

from geoluminate.contrib.organizations.models import Organization


class OrganizationListView(LoginRequiredMixin, ListView):
    model = Organization
    template_name = "user/organizations.html"
    context_object_name = "organizations"

    def get_queryset(self):
        return Organization.objects.filter(members__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Organizations")
        return context
