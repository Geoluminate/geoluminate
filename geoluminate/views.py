from auto_datatables.views import AutoTableMixin
from crispy_forms.helper import FormHelper
from django import forms
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as Model
from django.forms import modelform_factory
from django.urls import reverse
from django.utils.decorators import classonlymethod, method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, TemplateView, UpdateView
from django_filters.views import FilterView
from neapolitan.views import CRUDView, Role

from geoluminate.contrib.core.view_mixins import (
    BaseMixin,
    GeoluminatePermissionMixin,
    HTMXMixin,
    HTMXMixin2,
    ListFilterMixin,
)

GEOLUMINATE = settings.GEOLUMINATE


@method_decorator(cache_page(60 * 5), name="dispatch")
class BaseListView(BaseMixin, ListFilterMixin, HTMXMixin2, FilterView):
    """
    The base class for displaying a list of objects within the Geoluminate framework.
    """

    list_filter_top = ["title", "o"]

    def get_breadcrumbs(self):
        model = self.get_model()
        return [{"title": model._meta.verbose_name_plural, "url": reverse(f"{model._meta.model_name}-list")}]

    def get_model(self):
        return self.model or self.queryset.model


@method_decorator(cache_page(60 * 10), name="dispatch")
class BaseTableView(BaseMixin, AutoTableMixin, TemplateView):
    filter = None
    table_view_name = "sample-list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filter
        context["endpoint"] = self.get_table().url
        return context

    def get_table_url(self):
        if self.table_view_name and self.kwargs.get("pk"):
            model_name = self.model._meta.model_name
            return reverse(
                self.table_view_name,
                kwargs={f"{model_name}_uuid": self.kwargs.get("pk")},
            )
        return super().get_table_url()


class BaseDetailView(BaseMixin, HTMXMixin, GeoluminatePermissionMixin, DetailView):
    base = None
    base_template_suffix = "_detail.html"
    menu = []
    actions = []
    sidebar_components = [
        "core/sidebar/basic_info.html",
        "core/sidebar/keywords.html",
        "core/sidebar/status.html",
        "core/sidebar/summary.html",
    ]

    def get_object(self, queryset=None):
        """Returns the profile object."""
        return self.base.model.objects.get(pk=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["base"] = self.base
        context["base_model_name"] = self.base.model._meta.model_name
        context["base_model_verbose_name"] = self.base.model._meta.verbose_name
        context["base_model_name_plural"] = self.base.model._meta.verbose_name_plural
        context["page_menu"] = self.resolve_menu_urls()
        context["page_actions"] = self.resolve_action_urls()
        context["dates"] = self.get_dates()
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

    def resolve_menu_urls(self):
        """The menu item urls generated during the plugin registration process are not resolved until this method is called."""
        # tab = self.request.GET.get("tab", None)

        if not self.menu:
            raise NotImplementedError("You must define a menu attribute on the view.")
        for item in self.menu:
            item.resolved = reverse(item.url, kwargs={"pk": self.kwargs.get("pk")})
        return self.menu

    def resolve_action_urls(self):
        """The action item urls generated during the plugin registration process are not resolved until this method is called."""
        for item in self.actions:
            item.resolved = reverse(item.url, kwargs={"pk": self.kwargs.get("pk")})

        return self.actions


class BaseFormView(BaseMixin, HTMXMixin, LoginRequiredMixin, GeoluminatePermissionMixin):
    base_template = "geoluminate/base/form_view.html"
    template_name = "geoluminate/base/form_view.html"


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
            return ["geoluminate/forms/crispy.html#form"]
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

    def form_valid(self, form):
        # if self.request.htmx:
        # model_name = self.model._meta.model_name
        # template = f"{model_name}_form.html"

        # return render_to_response("geoluminate/forms/crispy.html", {"form": form})
        return super().form_valid(form)

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
