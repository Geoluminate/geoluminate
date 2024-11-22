from django.db.models.base import Model as Model
from django.http import Http404
from django.http.response import HttpResponse
from django.shortcuts import render
from django_htmx.http import retarget

from geoluminate.core.view_mixins import RelatedObjectMixin
from geoluminate.views import BaseCRUDView

from .forms import DateForm, DescriptionForm
from .models import Date, Description


class GenericCRUDView(RelatedObjectMixin, BaseCRUDView):
    base_object_url_kwarg = "object_id"

    def get_template_names(self):
        return [f"{self.template_name}#{self.template_name_suffix[1:]}"]

    def process_deletion(self, request, *args, **kwargs):
        """POST handler for the delete confirmation view."""
        self.object = self.get_object()
        self.object.delete()
        return self.remove_target()

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.content_object = self.base_object
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
        return self.base_object.descriptions.all()

    def get_create_context_data(self, context):
        dtype = self.request.GET.get("target")
        if not dtype:
            raise Http404("No description type specified")
        if dtype not in self.base_object.DESCRIPTION_TYPES.values:
            raise Http404("No such description type")

        if self.model.objects.filter(object_id=self.base_object.pk, type=dtype).exists():
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
        return self.base_object.dates.all()

    def get_create_context_data(self, context):
        dtype = self.request.GET.get("target")
        if not dtype:
            raise Http404("No date type specified")
        if dtype not in self.base_object.DATE_TYPES.values:
            raise Http404("No such date type")

        if self.model.objects.filter(object_id=self.base_object.pk, type=dtype).exists():
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
