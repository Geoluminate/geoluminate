from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as Model
from django.forms import modelform_factory
from django.urls import reverse
from django.utils.decorators import classonlymethod, method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, TemplateView, UpdateView
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

    list_filter_top = ["title", "o"]

    # def get_breadcrumbs(self):
    #     model = self.get_model()
    #     return [{"title": model._meta.verbose_name_plural, "url": reverse(f"{model._meta.model_name}-list")}]

    def get_model(self):
        return self.model or self.queryset.model


class BaseDetailView(BaseMixin, HTMXMixin, GeoluminatePermissionMixin, DetailView):
    base = None
    base_template_suffix = "_detail.html"

    def get_object(self, queryset=None):
        """Returns the profile object."""
        return self.base.model.objects.get(pk=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["base"] = self.base
        context["base_model_name"] = self.base.model._meta.model_name
        context["base_model_verbose_name"] = self.base.model._meta.verbose_name
        context["base_model_name_plural"] = self.base.model._meta.verbose_name_plural
        # context["dates"] = self.get_dates()
        return context

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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

    def register_template(self, template_name: str):
        return template_name
