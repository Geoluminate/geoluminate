from typing import Any, Dict, List, Optional, Type

from allauth.account.forms import AddEmailForm
from allauth.account.models import EmailAddress
from allauth.account.views import LoginView
from allauth.socialaccount.forms import DisconnectForm

# from allauth.account.adapter
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.forms import modelform_factory
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import resolve, reverse, reverse_lazy
from django.utils.encoding import force_str
from django.utils.translation import gettext as _
from django.views.generic import CreateView, ListView, TemplateView, UpdateView
from formset.views import (
    FileUploadMixin,
    FormCollectionViewMixin,
    FormView,
    FormViewMixin,
)

from geoluminate.contrib.contributors.models import Contributor
from geoluminate.contrib.core.views import CoreListView, HTMXMixin
from geoluminate.contrib.datasets.models import Dataset, Review
from geoluminate.contrib.organizations.forms import OrganisationFormCollection
from geoluminate.contrib.organizations.models import Organization
from geoluminate.contrib.projects.forms import ProjectForm
from geoluminate.contrib.projects.models import Project

from ..forms import UserProfileForm


class Dashboard(LoginRequiredMixin, HTMXMixin, TemplateView):
    htmx_template = "user/dashboard.html"


# ------------------ USER CONTRIBUTIONS ------------------
class BaseContributitionView(CoreListView):
    base_template = "user/base_list.html"

    def get_queryset(self):
        return super().get_queryset().filter(contributors__profile=self.request.user.profile)


user_projects_view = BaseContributitionView.as_view(model=Project, extra_context={"can_create": True})
user_datasets_view = BaseContributitionView.as_view(model=Dataset, extra_context={"can_create": True})


user_reviews_view = CoreListView.as_view(
    model=Review,
    base_template="user/base_list.html",
    object_template="user/review_card.html",
    extra_context={"can_create": True},
)


# class Reviews(CoreListView):
#     base_template = "user/base_list.html"

#     template_name = "user/contributor/projects.html"
#     form_class = ProjectForm
#     form_fields = ["title"]
#     title = _("Your Reviews")
#     success_url = "review-edit"

#     def get_queryset(self):
#         return self.request.user.profile.contributions.datasets()


# ------------------ PROFILE INFORMATION ------------------
class ProfileView(HTMXMixin, FileUploadMixin, FormViewMixin, LoginRequiredMixin, UpdateView):
    model = Contributor
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        obj, created = Contributor.objects.get_or_create(user=self.request.user)
        if created:
            self.request.user.save()
        return obj

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # if self.get_object():
        if self.object:
            context_data["change"] = True
        else:
            context_data["add"] = True
        context_data["title"] = _("Edit Profile")
        context_data["action"] = {
            "url": reverse("contributor:detail", kwargs={"pk": self.request.user.profile.pk}),
            "label": _("View Public Profile"),
        }
        return context_data

    def form_valid(self, form):
        if extra_data := self.get_extra_data():
            if extra_data.get("add") is True:
                form.instance.save()
            if extra_data.get("delete") is True:
                form.instance.delete()
                return JsonResponse({"success_url": self.get_success_url()})
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("contributor:detail", kwargs={"pk": self.request.user.profile.pk})


class AffiliationView(HTMXMixin, FormView):
    model = Organization
    form_class = OrganisationFormCollection
    template_name = "user/edit_affiliations.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = _("Edit Affiliations")
        return context_data


# ------------------ ACCOUNT SETTINGS ------------------


class Account(LoginRequiredMixin, TemplateView):
    template_name = "user/account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_add_email"] = EmailAddress.objects.can_add_email(self.request.user)
        context["forms"] = [
            (_("Password Reset"), "account/password_reset.html", DisconnectForm(request=self.request)),
        ]
        return context
