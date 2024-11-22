from django.contrib.auth.decorators import login_required
from django.db.models.base import Model as Model
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import DetailView
from django_filters.views import FilterView
from meta.views import MetadataMixin
from neapolitan.views import CRUDView

from geoluminate.contrib.identity.models import Database
from geoluminate.core.view_mixins import (
    HTMXMixin,
    ListFilterMixin,
)


@method_decorator(login_required, name="show_form")
class BaseCRUDView(MetadataMixin, HTMXMixin, CRUDView):
    ncols = 1
    object_template = None
    sidebar_fields = []
    menu = None
    path_converter = "str"

    # @property
    # def filterset_class(self):
    #     return self.model.get_filterset()

    def get_template_names(self):
        if self.template_name is not None:
            template_names = [self.template_name]

        if self.model is not None and self.template_name_suffix is not None:
            template_names = [
                f"{self.model._meta.app_label}/"
                f"{self.model._meta.object_name.lower()}"
                f"{self.template_name_suffix}.html",
                f"geoluminate/object{self.template_name_suffix}.html",
            ]

        return HTMXMixin.get_template_names(self, template_names)

    def get_list_context_data(self, context):
        context["filter_count"] = context["filterset"].qs.count()
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sidebar_fields"] = self.get_sidebar_fields()
        context["menu"] = self.menu
        context["object_template"] = self.get_object_template()
        func_name = f"get_{self.role.value}_context_data"
        if hasattr(self, func_name):
            context = getattr(self, func_name)(context)
        return context

    def get_object_template(self):
        if self.object_template:
            return self.object_template
        if hasattr(self.model, "get_inheritance_chain"):
            inherited_models = self.model.get_inheritance_chain()
            model_opts = [m._meta for m in inherited_models]
            return [f"{opts.app_label}/{opts.model_name}_card.html" for opts in model_opts]

        opts = self.model._meta if self.model else self.object_list.model._meta

        return [
            f"{opts.app_label}/{opts.model_name}_card.html",
            f"{opts.model_name}_card.html",
        ]

    def get_meta_title(self, context):
        value = context["object_verbose_name_plural"].capitalize()
        if self.role.value == "create":
            value = _(f"Create {self.model._meta.verbose_name}")
        if self.object:
            value = self.object
        if self.role.value == "edit":
            value = _(f"Edit {self.model._meta.verbose_name}")
        context["title"] = value
        return f"{value} · {Database.get_solo().safe_translation_getter('name')}"

    def get_sidebar_fields(self):
        return self.sidebar_fields


# @method_decorator(cache_page(60 * 5), name="dispatch")
class BaseListView(MetadataMixin, ListFilterMixin, HTMXMixin, FilterView):
    """
    The base class for displaying a list of objects within the Geoluminate framework.
    """

    template_name_suffix = "_list"
    ncols = 1

    def get_model(self):
        return self.model or self.queryset.model

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_verbose_name_plural"] = self.get_model()._meta.verbose_name_plural
        return context

    def get_template_names(self):
        if self.template_name is not None:
            template_names = [self.template_name]

        if self.model is not None and self.template_name_suffix is not None:
            template_names = [
                f"{self.model._meta.app_label}/"
                f"{self.model._meta.object_name.lower()}"
                f"{self.template_name_suffix}.html",
                f"geoluminate/object{self.template_name_suffix}.html",
            ]

        return HTMXMixin.get_template_names(self, template_names)


class BaseDetailView(MetadataMixin, HTMXMixin, DetailView):
    # base_model: models.Model = None
    model = None
    sidebar_fields = []
    menu = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sidebar_fields"] = self.sidebar_fields
        context["menu"] = self.menu
        return context
