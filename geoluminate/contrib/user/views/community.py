from typing import Any, Dict, List

from allauth.account.forms import AddEmailForm
from allauth.account.models import EmailAddress
from allauth.account.views import LoginView
from allauth.socialaccount.forms import DisconnectForm

# from allauth.account.adapter
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.translation import gettext as _
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from formset.views import (
    FileUploadMixin,
    FormCollectionViewMixin,
    FormView,
    FormViewMixin,
)
from organizations.models import Organization

from geoluminate.contrib.project.tables import DatasetTable, ProjectTable
from geoluminate.tables import ClientSideProcessing
from geoluminate.views import GeoluminateTableView

from ..forms import UserForm, UserProfileForm
from ..models import Profile, User
from ..tables import Datasets, Projects


class CommunityView(LoginRequiredMixin, TemplateView):
    template_name = "user/community.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context


class CommunityDirectoryView(LoginRequiredMixin, GeoluminateTableView):
    table_config_class = ClientSideProcessing
    model = Profile
    fields = [
        "name",
        "about",
    ]
    row_template_name = "geoluminate/datatables/profile_item.html"


class MemberProfileView(DetailView):
    model = Profile
    template_name = "user/member_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tables"] = {
            "projects": ProjectTable(
                url=reverse("contributor-projects-list", kwargs={"contributor_pk": self.object.pk}),
                config_class=ClientSideProcessing(buttons=[], dom="pt"),
                layout_overrides={},
            ),
            "datasets": DatasetTable(
                url=reverse("contributor-datasets-list", kwargs={"contributor_pk": self.object.pk}),
                config_class=ClientSideProcessing(buttons=[], dom="pt"),
                layout_overrides={},
            ),
        }
        return context
