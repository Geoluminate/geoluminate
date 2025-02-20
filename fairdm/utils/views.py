from actstream import actions
from actstream.models import Follow
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as Model
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django_contact_form.views import ContactFormView
from literature.models import LiteratureItem

from fairdm.contrib import CORE_MAPPING
from fairdm.core.forms import DatasetForm, ProjectForm
from fairdm.registry import registry
from fairdm.views import FairDMListView

from .filters import LiteratureFilterset


class ReferenceListView(FairDMListView):
    title = _("References")
    model = LiteratureItem
    paginate_by = 20
    filterset_class = LiteratureFilterset
    template_name = "fairdm/object_list.html"
    # def get_template_names(self):
    #     return ["fairdm/object_list.html"]


def follow_unfollow(request, pk):
    model_class = apps.get_model(CORE_MAPPING[pk[0]])
    instance = get_object_or_404(model_class, pk=pk)
    is_following = Follow.objects.is_following(request.user, instance)

    if is_following:
        actions.unfollow(request.user, instance)
    else:
        actions.follow(request.user, instance)
    return HttpResponse(status=200)


class GenericContactForm(LoginRequiredMixin, ContactFormView):
    """A view class that will send an email to all contributors with the ContactPerson role."""

    def get_object(self, queryset=None):
        model_class = apps.get_model(CORE_MAPPING[self.kwargs["object_type"]])
        return model_class.objects.get(pk=self.kwargs["pk"])

    @property
    def recipient_list(self):
        self.object = self.get_object()

        contacts = self.object.contributors.filter(roles__contains=["ContactPerson"])

        # get the email addresses of the contributors
        emails = []
        for c in contacts:
            if c.profile.user:
                emails.append(c.profile.user.email)
        return emails


class DirectoryView(RedirectView):
    """
    Redirects shortened URLs to full, descriptive URLs for various object types.

    E.g. /p1234567890abcdef/ -> /project/p1234567890abcdef/
    or /s1234567890abcdef/ -> /sample/s1234567890abcdef/
    """

    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs["uuid"]
        model = apps.get_model(CORE_MAPPING[pk[0]])
        obj = get_object_or_404(model, pk=pk)
        return obj.get_absolute_url()


class HomeView(TemplateView):
    template_name = "fairdm/pages/home.html"
    authenticated_template = "dashboard.html"

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return self.authenticated_template
        return super().get_template_names()

    def authenticated_context(self, context, **kwargs):
        context["forms"] = {
            "project": ProjectForm(),
            "dataset": DatasetForm(),
        }
        return context

    def anonymous_context(self, context, **kwargs):
        context["registry"] = registry
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            return self.authenticated_context(context, **kwargs)
        return self.anonymous_context(context, **kwargs)
