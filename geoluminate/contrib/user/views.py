from typing import Any, Dict

from allauth.account.forms import AddEmailForm
from allauth.account.models import EmailAddress
from allauth.account.views import LoginView
from allauth.socialaccount.forms import DisconnectForm
from auto_datatables.mixins import AjaxMixin
from auto_datatables.tables import BaseDataTable
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.generic import ListView, TemplateView, UpdateView
from formset.views import FileUploadMixin, FormCollectionViewMixin, FormViewMixin

from geoluminate.contrib.project.models import Project
from geoluminate.contrib.project.views.project import ProjectForm

from .forms import UserForm, UserProfileForm
from .models import Profile


class Account(LoginRequiredMixin, TemplateView):
    template_name = "user/account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_add_email"] = EmailAddress.objects.can_add_email(self.request.user)
        context["forms"] = [
            (_("E-mail Addresses"), "account/email.html", AddEmailForm(self.request)),
            (_("Password Reset"), "account/password_reset.html", DisconnectForm(request=self.request)),
            (_("Account Connections"), "socialaccount/connections.html", AddEmailForm(self.request)),
        ]
        return context


class ProfileView(FileUploadMixin, FormViewMixin, LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "user/profile_edit.html"
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        return self.request.user

    # def get_success_url(self):
    # return reverse_lazy('profile', kwargs={'profile_slug': self.request.user.userpofile.slug})

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     c_def = self.get_user_context(title='Settings')

    # def get_object(self, queryset=None):
    #     if self.extra_context["add"] is False:
    #         return super().get_object(queryset)

    def form_valid(self, form):
        if extra_data := self.get_extra_data() and extra_data.get("delete") is True:
            self.object.delete()
            success_url = self.get_success_url()
            response_data = {"success_url": force_str(success_url)} if success_url else {}
            return JsonResponse(response_data)
        return super().form_valid(form)


class UserProjectListView(LoginRequiredMixin, ListView):
    template_name = "project/list.html"
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ProjectForm()
        return context

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)


class CommunityView(LoginRequiredMixin, TemplateView):
    template_name = "user/community.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context


class CommunityDirectoryView(BaseDataTable, AjaxMixin):
    model = Profile
    fields = [
        "name",
        "about",
    ]
    row_template_name = "geoluminate/datatables/profile_item.html"
    paging = False
    search_fields = ["name"]
    # fields = ["name", "about", "status", "date_joined", ]
    fixedHeader = True
    # dom = "rsti"
    app_name = "user"
