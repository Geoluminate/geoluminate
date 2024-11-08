from django.db.models.base import Model as Model
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView
from django_filters.views import FilterView
from meta.views import MetadataMixin
from neapolitan.views import CRUDView

from geoluminate.core.views.mixins import (
    HTMXMixin,
    ListFilterMixin,
)
from geoluminate.identity.models import Database


class BaseCRUDView(MetadataMixin, HTMXMixin, CRUDView):
    ncols = 1
    object_template = None
    sidebar_fields = []
    menu = None
    path_converter = "str"

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


@method_decorator(cache_page(60 * 5), name="dispatch")
class BaseListView(MetadataMixin, ListFilterMixin, HTMXMixin, FilterView):
    """
    The base class for displaying a list of objects within the Geoluminate framework.
    """

    ncols = 1
    list_filter_top = ["title", "o"]

    def get_model(self):
        return self.model or self.queryset.model


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
