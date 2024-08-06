from typing import Any

from django.apps import apps
from django.db import models
from django.db.models import QuerySet
from django.urls import reverse
from el_pagination.views import AjaxMultipleObjectTemplateResponseMixin
from meta.views import MetadataMixin


class HTMXMixin2:
    """Adds HTMX support to a class-based view using django-template-partials. A fragment can be passed in the request using the 'fragment' query parameter. If the request is an HTMX request, the template_name attribute is used to render the view. Otherwise, the base_template attribute is used."""

    base_template: str | None = None

    def get_template_names(self):
        template_names = [*super().get_template_names(), self.base_template]
        # get fragment from request
        fragment = self.request.GET.get("fragment", None)
        if fragment:
            template_names = [f"{t}#{fragment}" for t in template_names]

        return template_names

    # def discover_templates(self):
    #     """Follows the "extends" chain to discover the templates that are used to render the view."""
    #     # django-template-partials will only look for partials in the direct template (e.g. it will not look in base templates)
    #     # it does accept a list of template names
    #     template_name = self.template
    #     template = get_template(template_name)

    #     source = template.source


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
    base_template = "geoluminate/base/list_view.html"
    page_template = "geoluminate/base/list_view.html#card"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # the template to be used for displaying individual objects in the list
        context["object_template"] = self.get_object_template()
        # normally, this is handled by the get method on el_pagination.views.AjaxListView but that conflicts with FilterView.
        # context["page_template"] = self.page_template
        context["total_object_count"] = self.get_queryset().count()
        context["page_size"] = self.page_size
        context["col"] = 12 // self.columns

        return context

    def get_object_template(self):
        opts = self.model._meta if self.model else self.object_list.model._meta
        templates = [
            f"{opts.app_label}/{opts.model_name}_card.html",
            f"{opts.model_name}_card.html",
        ]

        if template := getattr(self, "object_template", None):
            templates.insert(0, template)

        return templates


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
    template_name = "geoluminate/base/list_view.html#page"
    create_view_name = ""

    def dispatch(self, request, *args, **kwargs):
        self.related_model = kwargs.pop("related_model", None)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = self.get_queryset()
        context["create_url"] = self.get_create_url()
        return context

    def get_create_url(self):
        if self.create_view_name:
            return reverse(self.create_view_name)
        else:
            model_name = self.get_queryset().model._meta.model_name
            # kwargs.update({"model": model_name[0]})
            return reverse(f"{model_name}-create", kwargs=self.kwargs)


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
        return False or self.request.user.is_superuser

    def has_edit_permission(self):
        return False or self.request.user.is_superuser

    def has_delete_permission(self):
        return False or self.request.user.is_superuser

    def has_view_permission(self):
        return False or self.request.user.is_superuser

    def has_detail_permission(self):
        return False or self.request.user.is_superuser

    def has_list_permission(self):
        return False or self.request.user.is_superuser

    def has_permission(self, action: str):
        return getattr(self, f"has_{action}_permission")()


class BaseMixin(MetadataMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if getattr(self, "queryset", None):
            context["model_name"] = self.queryset.model._meta.verbose_name
            context["model_name_plural"] = self.queryset.model._meta.verbose_name_plural
        elif getattr(self, "model", None):
            context["model_name"] = self.model._meta.verbose_name
            context["model_name_plural"] = self.model._meta.verbose_name_plural
        context["breadcrumbs"] = self.get_breadcrumbs()
        return context

    def get_breadcrumbs(self):
        return []
