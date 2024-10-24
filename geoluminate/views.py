from typing import Any

from crispy_forms.helper import FormHelper
from django import forms
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models import QuerySet
from django.db.models.base import Model as Model
from django.forms import modelform_factory
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import classonlymethod, method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, UpdateView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django_filters.views import FilterView
from neapolitan.views import CRUDView, Role

from geoluminate.core.views.mixins import (
    BaseMixin,
    GeoluminatePermissionMixin,
    HTMXMixin,
    HTMXMixin2,
    ListFilterMixin,
)
from geoluminate.models import Measurement, Sample


@method_decorator(cache_page(60 * 5), name="dispatch")
class BaseListView(BaseMixin, ListFilterMixin, HTMXMixin2, FilterView):
    """
    The base class for displaying a list of objects within the Geoluminate framework.
    """

    ncols = 1
    list_filter_top = ["title", "o"]

    def get_model(self):
        return self.model or self.queryset.model


class BaseDetailView(BaseMixin, GeoluminatePermissionMixin, SingleObjectTemplateResponseMixin):
    base_template_suffix = "_detail.html"
    base_template: str | None = None
    base_template_suffix: str = ".html"
    template_name: str | None = None
    object_list: QuerySet | None = None
    base_model: models.Model = None
    core_mapping = {
        "p": "projects.Project",
        "d": "datasets.Dataset",
        "s": "samples.Sample",
        "m": "measurements.Measurement",
        "c": "contributors.Contributor",
    }

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        if mtype := self.core_mapping.get(pk[0], None):
            self.base_model = apps.get_model(mtype)
        else:
            raise Http404("Object does not exist")
        if hasattr(self.base_model, "polymorphic_model_marker"):
            self.base_object = get_object_or_404(self.base_model.objects.non_polymorphic(), pk=pk)
        else:
            self.base_object = get_object_or_404(self.base_model, pk=pk)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["base_model"] = self.base_model
        context["base_model_name"] = self.base_model._meta.verbose_name
        context["base_model_name_plural"] = self.base_model._meta.verbose_name_plural
        context["base_object"] = self.base_object
        context[self.base_model._meta.model_name] = self.base_object
        # context["template_name"] = self.get_template_names()
        context["template_name"] = self.template_name
        return context

    def get_base_template(self, **kwargs: Any) -> list[str]:
        """
        Returns the base template name based on the model's meta information and the requesting app's name.
        """
        opts = self.base_model._meta

        requesting_app_name = self.request.resolver_match.app_name
        names = [
            f"{requesting_app_name}/base{self.base_template_suffix}",
            # f"{opts.app_label}/{opts.model_name}{self.base_template_suffix}",
            f"{opts.app_label}/base{self.base_template_suffix}",
            # f"{opts.app_label}/{opts.model_name}_base.html",
            f"base{self.base_template_suffix}",
            "base.html",
        ]
        if base_template := self.kwargs.get("base_template") or self.base_template:
            names.insert(0, base_template)
        return names

    def get_template_names(self) -> list[str]:
        """
        Returns the template name. If the request is an HTMX request, it returns `self.template_name`. Otherwise, it returns the result of `self.get_base_template()`.
        """
        if self.request.htmx:
            return [self.template_name]
        return self.get_base_template()

    def get_dates(self):
        output = {}
        for val, display in self.object.dates.model.type_vocab.choices:
            date = {
                "label": display,
                "value": "-",  # default value
            }
            output[val] = date

        for date in self.object.dates.all():
            output[date.type]["value"] = date.date

        return output


class BaseFormView(BaseMixin, HTMXMixin, LoginRequiredMixin, GeoluminatePermissionMixin):
    base_template = "geoluminate/base/form.html"
    template_name = "geoluminate/base/form.html#form"


class BaseEditView(BaseMixin, LoginRequiredMixin, GeoluminatePermissionMixin, CRUDView):
    related_name = ""
    path_converter = "uuid"

    @classmethod
    def __getattr__(cls, name):
        if name == "lookup_url_kwarg":
            return str(cls.model._meta.model_name + "_pk")
        return super().__getattr__(name)

    def get_template_names(self) -> list[str]:
        """
        Returns the template name. If the request is an HTMX request, it returns `self.template_name`. Otherwise, it returns the result of `self.get_base_template()`.
        """
        template_names = super().get_template_names()
        fragment = "form"
        if self.request.htmx:
            template_names = [f"{t}#{fragment}" for t in template_names]
            return ["geoluminate/base/form.html#form"]
        return template_names

    def get_form_class(self):
        form_class = super().get_form_class()
        fields = self.request.GET.get("fields", None)
        if fields:
            fields = fields.split(",")
            fields.append(self.related_name)
            if not all(f in form_class.Meta.fields for f in fields):
                raise ValueError("Invalid fields specified in query string.")
        return modelform_factory(self.model, form=form_class, fields=fields)

    def get_form(self, data=None, files=None, **kwargs):
        """
        Returns a form instance.
        """
        cls = self.get_form_class()
        # self.related = self.get_related_object()

        if has_related := self.kwargs.get("pk") and self.related_name:
            kwargs.update(initial={self.related_name: self.kwargs.get("pk")})

        form = cls(data=data, files=files, **kwargs)
        if has_related:
            print("has_related", has_related, self.related_name, self.kwargs.get("pk"))
            form.fields[self.related_name].widget = forms.HiddenInput()

        # a form ID is required to have the submit button outside the form (e.g. in a modal footer)
        # therefore we make sure the form has a helper and a form_id attribute
        if not hasattr(form, "helper"):
            form.helper = FormHelper()
        if not hasattr(form.helper, "form_id"):
            form.helper.form_id = f"{self.model._meta.model_name}-form"

        # must be True otherwise hidden fields will not be rendered and data from those fields will not be submitted (causing validation errors)
        form.helper.render_hidden_fields = True

        if self.role == Role.CREATE:
            form.helper.form_action = reverse(f"{self.url_base}-create", kwargs=self.kwargs)
            # form.helper.form_action = self.role.maybe_reverse(self)
        # elif self.role == Role.UPDATE:
        # form.helper.form_action = reverse(f"{self.url_base}-update", kwargs=self.kwargs)
        return form

    def get_fields(self):
        fields = self.request.GET.get("fields", None)
        if fields:
            return fields.split(",")

    def get_success_url(self):
        related = getattr(self.object, self.related_name)
        return related.get_absolute_url()

    @classonlymethod
    def get_urls(cls, model=None, roles=None):
        """Classmethod to generate URL patterns for the view."""
        if model is not None:
            cls.model = model
        if roles is None:
            roles = [Role.CREATE, Role.UPDATE, Role.DELETE]

        return [role.get_url(cls) for role in roles]


class BaseUpdateView(BaseFormView, UpdateView):
    pass


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
