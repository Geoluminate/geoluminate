from typing import Any

from django.apps import apps
from django.db import models
from django.db.models import QuerySet
from el_pagination.views import AjaxMultipleObjectTemplateResponseMixin
from meta.views import MetadataMixin


class HTMXMixin:
    """
    A Django class-based view mixin for handling HTMX requests. It requires a base template that is rendered when the request is not an HTMX request. When the request is HTMX, the template_name attribute is used to render the view.

    .. note::

    The base template must utilize {% include template_name %} somewhere in the template. The template_name attribute is used to render the view when the request is an HTMX request.

    Attributes:
        base_template (str): The base template name to be used for rendering the view.
        base_template_suffix (str): The suffix to be added to the base template name.
        template_name (str): The name of the template to be used for rendering the view.
        object_list (QuerySet): The list of objects to be displayed in the view.
    """

    base_template: str | None = None
    base_template_suffix: str = ".html"
    template_name: str | None = None
    object_list: QuerySet | None = None
    model: models.Model = None

    def get_base_template(self, **kwargs: Any) -> list[str]:
        """
        Returns the base template name based on the model's meta information and the requesting app's name.
        """
        opts = self.model._meta if self.model else self.object_list.model._meta

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
            print("htmx", self.template_name)
            return self.template_name
        print("not htmx", self.get_base_template())
        return self.get_base_template()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        Adds the result of get_template_names to the view context as template_name.
        """
        context = super().get_context_data(**kwargs)
        context["template_name"] = super().get_template_names()
        return context


class ListMixin(AjaxMultipleObjectTemplateResponseMixin):
    page_size = 20
    columns: int = 1

    template_name = "geoluminate/base/list_view.html"
    page_template = "geoluminate/base/card_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # the template to be used for displaying individual objects in the list
        context["object_template"] = self.object_template

        # normally, this is handled by the get method on el_pagination.views.AjaxListView but that conflicts with FilterView.
        context["page_template"] = self.page_template
        context["total_object_count"] = self.get_queryset().count()
        context["page_size"] = self.page_size
        context["col"] = 12 // self.columns

        return context


class ListFilterMixin(ListMixin):
    list_filter_top: list[str] = []

    def get_filterset_class(self):
        """
        Returns the filterset class to use in this view
        """
        model = self.get_queryset().model
        model_name = model._meta.model_name
        app_config = apps.get_app_config(model._meta.app_label)
        if model_config := getattr(app_config, model_name, {}):
            self.filterset_class = model_config.get("filterset_class", self.filterset_class)
            self.filterset_fields = model_config.get("filterset_fields", self.filterset_fields)
        return super().get_filterset_class()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if context["object_list"] is not None:
            context["filtered_object_count"] = context["object_list"].count()
        context["is_filtered"] = hasattr(context["filter"].form, "cleaned_data")
        context["list_filter_top"] = self.list_filter_top
        return context


class ListPluginMixin(ListMixin):
    template_name = "geoluminate/plugins/base_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = self.get_queryset()
        return context


class GeoluminatePermissionMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_has_permission"] = {
            "create": self.has_create_permission(),
            "edit": self.has_edit_permission(),
            "delete": self.has_delete_permission(),
            "view": self.has_view_permission(),
            "detail": self.has_detail_permission(),
            "list": self.has_list_permission(),
        }
        return context

    def has_create_permission(self):
        return False

    def has_edit_permission(self):
        return False

    def has_delete_permission(self):
        return False

    def has_view_permission(self):
        return False

    def has_detail_permission(self):
        return False

    def has_list_permission(self):
        return False

    def has_permission(self, action: str):
        return getattr(self, f"has_{action}_permission")()


class BaseMixin(MetadataMixin):
    pass
