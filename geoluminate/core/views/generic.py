from actstream import actions
from actstream.models import Follow
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as Model
from django.http import Http404
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django_contact_form.views import ContactFormView
from django_htmx.http import retarget

from geoluminate.contrib import CORE_MAPPING
from geoluminate.models import Measurement, Sample
from geoluminate.views import BaseCRUDView

from ..forms import DateForm, DescriptionForm
from ..models import Date, Description
from .mixins import BaseObjectMixin


def follow_unfollow(request, pk):
    model_class = apps.get_model(CORE_MAPPING[pk[0]])
    instance = get_object_or_404(model_class, pk=pk)
    is_following = Follow.objects.is_following(request.user, instance)

    if is_following:
        actions.unfollow(request.user, instance)
    else:
        actions.follow(request.user, instance)
    return HttpResponse(status=200)


class GenericCRUDView(BaseObjectMixin, BaseCRUDView):
    def get_template_names(self):
        return [f"{self.template_name}#{self.template_name_suffix[1:]}"]

    def process_deletion(self, request, *args, **kwargs):
        """POST handler for the delete confirmation view."""
        self.object = self.get_object()
        self.object.delete()
        return self.remove_target()

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.content_object = self.get_base_object()
        self.object.save()
        response = render(self.request, f"{self.template_name}#detail", {"description": self.object})
        return self.send_response(response)

    def send_response(self, response):
        if self.object:
            return retarget(response, f"#{ self.object.type }-description")
        return retarget(response, f"#{ self.object.type }-description")

    def remove_target(self):
        return self.send_response(HttpResponse(status=200))


class DescriptionCRUDView(GenericCRUDView):
    model = Description
    form_class = DescriptionForm
    htmx_fragment = "form"
    template_name = "core/description.html"

    def get_queryset(self):
        return self.get_base_object().descriptions.all()

    def get_create_context_data(self, context):
        dtype = self.request.GET.get("target")
        if not dtype:
            raise Http404("No description type specified")
        if dtype not in self.get_base_object().DESCRIPTION_TYPES.values:
            raise Http404("No such description type")

        if self.model.objects.filter(object_id=self.get_base_object().pk, type=dtype).exists():
            raise Http404("Description type already exists")

        context["title"] = self.request.GET.get("target")
        return context

    def get_update_context_data(self, context):
        context["title"] = context["form"].initial["type"]
        return context

    def get_form(self, data=None, files=None, **kwargs):
        cls = self.get_form_class()
        if self.role.value == "create":
            kwargs["initial"] = {"type": self.request.GET.get("target")}
        return cls(data=data, files=files, **kwargs)

    def form_valid(self, form):
        if not form.cleaned_data.get("value"):
            if form.instance.pk:
                self.process_deletion(self.request)
            return retarget(HttpResponse(status=200), f"#{ form.cleaned_data.get('type') }-description")
        return super().form_valid(form)

    def form_invalid(self, form):
        response = render(self.request, f"{self.template_name}#form", {"form": form})
        dtype = form.data.get("type")
        return retarget(response, f"#{ dtype }-description")


class DatesCRUDView(GenericCRUDView):
    model = Date
    form_class = DateForm
    htmx_fragment = "form"
    template_name = "core/date.html"

    def get_queryset(self):
        return self.get_base_object().dates.all()

    def get_create_context_data(self, context):
        dtype = self.request.GET.get("target")
        if not dtype:
            raise Http404("No date type specified")
        if dtype not in self.get_base_object().DATE_TYPES.values:
            raise Http404("No such date type")

        if self.model.objects.filter(object_id=self.get_base_object().pk, type=dtype).exists():
            raise Http404("Description type already exists")

        context["title"] = self.request.GET.get("target")
        return context

    def get_update_context_data(self, context):
        context["title"] = context["form"].initial["type"]
        return context

    def get_form(self, data=None, files=None, **kwargs):
        cls = self.get_form_class()
        if self.role.value == "create":
            kwargs["initial"] = {"type": self.request.GET.get("target")}
        return cls(data=data, files=files, **kwargs)

    def form_valid(self, form):
        if not form.cleaned_data.get("value"):
            if form.instance.pk:
                self.process_deletion(self.request)
            return retarget(HttpResponse(status=200), f"#{ form.cleaned_data.get('type') }")
        return super().form_valid(form)

    def form_invalid(self, form):
        response = render(self.request, f"{self.template_name}#form", {"form": form})
        dtype = form.data.get("type")
        return retarget(response, f"#{ dtype }-description")


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
    permanent = False
    prefix_map = {
        "p": "projects.Project",
        "d": "datasets.Dataset",
        "s": "samples.Sample",
        # "m": "measurements.Measurement",
        "c": "contributors.Contributor",
    }

    def get_redirect_url(self, *args, **kwargs):
        obj_id = self.kwargs.get("pk")

        model_name = self.prefix_map[obj_id[0]]

        model = apps.get_model(model_name)

        obj = model.objects.get(pk=obj_id)

        self.url = obj.get_absolute_url()
        return super().get_redirect_url(*args, **kwargs)


class HomeView(TemplateView):
    template_name = "home.html"
    authenticated_template = "dashboard.html"

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return self.authenticated_template
        return super().get_template_names()

    def authenticated_context(self, context, **kwargs):
        return context

    def anonymous_context(self, context, **kwargs):
        result = []
        for stype in Sample.get_subclasses():
            metadata = stype.get_metadata()
            # metadata["detail_url"] = reverse(self.detail_url, kwargs={"subclass": stype._meta.model_name.lower()})
            # metadata["list_url"] = reverse(self.list_url, kwargs={"subclass": stype._meta.model_name.lower()})
            result.append(metadata)

        context["sample_types"] = result

        result = []
        for stype in Measurement.get_subclasses():
            metadata = stype.get_metadata()
            # metadata["detail_url"] = reverse(self.detail_url, kwargs={"subclass": stype._meta.model_name.lower()})
            # metadata["list_url"] = reverse(self.list_url, kwargs={"subclass": stype._meta.model_name.lower()})
            result.append(metadata)

        context["measurement_types"] = result

        # context["measurement_types"] = MeasurementType.objects.all()
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            return self.authenticated_context(context, **kwargs)
        return self.anonymous_context(context, **kwargs)
