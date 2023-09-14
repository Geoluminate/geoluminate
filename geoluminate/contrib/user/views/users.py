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
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_str
from django.utils.translation import gettext as _
from django.views.generic import CreateView, ListView, TemplateView, UpdateView
from formset.views import (
    FileUploadMixin,
    FormCollectionViewMixin,
    FormView,
    FormViewMixin,
)
from organizations.models import Organization

from geoluminate.contrib.core.forms import DatasetForm, ProjectForm
from geoluminate.contrib.core.models import Dataset, Project
from geoluminate.contrib.core.views.base import ContributionView

from ..forms import OrganisationFormCollection, UserForm, UserProfileForm
from ..models import Contributor, User
from ..tables import Datasets, Projects


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "user/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Account(LoginRequiredMixin, TemplateView):
    template_name = "user/account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_add_email"] = EmailAddress.objects.can_add_email(self.request.user)
        context["forms"] = [
            (_("Password Reset"), "account/password_reset.html", DisconnectForm(request=self.request)),
        ]
        return context


class ProfileView(FileUploadMixin, FormViewMixin, LoginRequiredMixin, UpdateView):
    model = Contributor
    form_class = UserProfileForm
    template_name = "user/profile_edit.html"

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
            "url": reverse("community:profile", kwargs={"pk": self.request.user.profile.pk}),
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
        return reverse("community:profile", kwargs={"pk": self.request.user.profile.pk})


class UserProjects(ContributionView):
    template_name = "user/contributor/projects.html"
    form_class = ProjectForm
    form_fields = ["title"]
    title = _("Your Projects")
    success_url = "project-edit"
    model = Contributor

    def get_object(self):
        return self.request.user.profile

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        # add the current user as a contributor
        self.object.contributors.create(
            roles="ProjectLeader,ProjectMember",
            profile=self.request.user.profile,
        )

        # self.object.contributors.create(
        #     roles="HostingInstitution",
        #     profile=self.request.user.default_affiliation.profile,
        # )

        # self.object.contributors.c(self.request.user.profile)

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # kwargs["instance"] = Project(
        #     contributors=[self.get_object()],
        # )
        return kwargs


class UserDatasets(ContributionView):
    template_name = "user/contributor/projects.html"
    # form_class = DatasetForm
    form_fields = ["title"]
    title = _("Your Datasets")
    success_url = "dataset-edit"
    model = Dataset

    def get_object(self, queryset):
        return self.request.user.profile

    # def get_queryset(self):
    #     return self.request.user.profile.get_datasets()


class Reviews(ContributionView):
    template_name = "user/contributor/projects.html"
    form_class = ProjectForm
    form_fields = ["title"]
    title = _("Your Reviews")
    success_url = "review-edit"

    def get_queryset(self):
        return self.request.user.profile.get_datasets()


class AffiliationView(FormView):
    model = Organization
    form_class = OrganisationFormCollection
    template_name = "user/edit_affiliations.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = _("Edit Affiliations")
        return context_data
