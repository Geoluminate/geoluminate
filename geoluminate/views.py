from typing import Any, Dict, List, Optional

from auto_datatables.views import AutoTableMixin
from django.apps import apps
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import resolve, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin, RedirectView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView as GenericFormView
from django.views.generic.edit import UpdateView
from django_filters.views import FilterView
from el_pagination.views import AjaxMultipleObjectTemplateResponseMixin
from meta.views import MetadataMixin

GEOLUMINATE = getattr(settings, "GEOLUMINATE")


class DashboardRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("contributor:detail", kwargs={"uuid": self.request.user.profile.uuid})


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

    base_template: Optional[str] = None
    base_template_suffix: str = ".html"
    template_name: Optional[str] = None
    object_list: Optional[QuerySet] = None

    def get_base_template(self, **kwargs: Any) -> List[str]:
        """
        Returns the base template name based on the model's meta information and the requesting app's name.
        """
        opts = self.model._meta if getattr(self, "model") else self.object_list.model._meta

        requesting_app_name = self.request.resolver_match.app_name
        names = [
            # f"{requesting_app_name}/base{self.base_template_suffix}",
            # f"{opts.app_label}/{opts.model_name}{self.base_template_suffix}",
            f"{opts.app_label}/base{self.base_template_suffix}",
            # f"{opts.app_label}/{opts.model_name}_base.html",
            f"base{self.base_template_suffix}",
            "base.html",
        ]
        print(self.base_template)
        if base_template := self.kwargs.get("base_template") or self.base_template:
            names.insert(0, base_template)
        print(names)
        return names

    def get_template_names(self) -> List[str]:
        """
        Returns the template name. If the request is an HTMX request, it returns `self.template_name`. Otherwise, it returns the result of `self.get_base_template()`.
        """
        if self.request.htmx:
            return self.template_name
        return self.get_base_template()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Adds the result of get_template_names to the view context as template_name.
        """
        context = super().get_context_data(**kwargs)
        context["template_name"] = super().get_template_names()
        return context


@method_decorator(cache_page(60 * 5), name="dispatch")
class BaseListView(MetadataMixin, AjaxMultipleObjectTemplateResponseMixin, HTMXMixin, FilterView):
    """
    The base class for displaying a list of objects within the Geoluminate framework.

    This view includes several mixins to provide additional functionality:
    - MetadataMixin: Adds SEO metadata to the view.
    - AjaxMultipleObjectTemplateResponseMixin: Allows the view to handle AJAX requests and return multiple objects.
    - HTMXMixin: Adds support for HTMX requests.
    - FilterView: Adds support for filtering the list of objects.

    Attributes:
        base_template_suffix (str): The suffix to be added to the base template name.
        object_template (str): The name of the template to be used for each object in the list.
        object_template_suffix (str): The suffix to be added to the object template name.
        template_name (str): The name of the template to be used for rendering the view.
        page_template (str): The name of the template to be used for pagination.
        page_size (int): The number of objects to display per page.
        columns (int): The number of columns to display in the list.
        list_filter_top (list): The list of filter fields to display at the top of the entry list.

    Methods:
        get_meta_title(context): Returns the title to be used in the meta tags.
        get_filterset_class(): Returns the filterset class to use in this view.
        get_object_template(**kwargs): Returns the template name to be used for each object in the list.
        get_context_data(**kwargs): Returns the context data for rendering the view.
        has_create_permission(): Returns True if the user has permission to add new objects.
    """

    base_template_suffix = "_list.html"
    object_template = None
    object_template_suffix = "_card.html"
    template_name = "geoluminate/base/list_view.html"
    page_template = "geoluminate/base/card_list.html"
    page_size = 20
    columns: int = 1
    list_filter_top = ["title", "status", "o"]

    def get_meta_title(self, context=None):
        title = super().get_meta_title(context) or self.object_list.model._meta.verbose_name_plural
        db_name = GEOLUMINATE.get("database").get("acronym")
        return f"{db_name} {title.title()}"

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

    def get_object_template(self, **kwargs):
        """Return the template name used for each object in the object_list for loop."""
        opts = self.object_list.model._meta
        # return f"{opts.app_label}/{opts.model_name}{self.object_template_suffix}"
        return f"{opts.model_name}s/{opts.model_name}{self.object_template_suffix}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # the template to be used for displaying individual objects in the list
        context["object_template"] = self.object_template or self.get_object_template()

        # normally, this is handled by the get method on el_pagination.views.AjaxListView but that conflicts with FilterView.
        context["page_template"] = self.page_template
        context["total_object_count"] = self.get_queryset().count()
        context["filtered_object_count"] = context["object_list"].count()
        context["can_create"] = self.kwargs.get("can_create", False)
        context["page_size"] = self.page_size
        context["is_filtered"] = hasattr(context["filter"].form, "cleaned_data")
        context["col"] = 12 // self.columns
        context["has_create_permission"] = self.has_create_permission()

        context["list_filter_top"] = self.list_filter_top

        return context

    def has_create_permission(self):
        """Returns True if the user has permission to add new objects."""
        return False


class BaseTableView(MetadataMixin, AutoTableMixin, TemplateView):
    filter = None
    table_view_name = "sample-list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filter
        return context

    def get_table_url(self):
        if self.table_view_name and self.kwargs.get("uuid"):
            model_name = self.model._meta.model_name
            return reverse(self.table_view_name, kwargs={f"{model_name}_uuid": self.kwargs.get("uuid")})
        return super().get_table_url()


class BaseDetailView(MetadataMixin, HTMXMixin, SingleObjectMixin):
    # base_template = "geoluminate/base/base_detail.html"
    base_template_suffix = "_detail.html"
    menu = []
    actions = []
    htmx = {
        # "target": "#contribPage",
    }
    allow_discussion = True
    sidebar_components = [
        "core/sidebar/basic_info.html",
        "core/sidebar/keywords.html",
        "core/sidebar/status.html",
        "projects/sidebar/summary.html",
    ]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """Returns the profile object."""
        return self.model.objects.get(uuid=self.kwargs.get("uuid"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_menu"] = self.resolve_menu_urls()
        context["page_actions"] = self.resolve_action_urls()
        context["htmx"] = self.htmx
        context["has_edit_permission"] = self.has_edit_permission()
        context["allow_discussion"] = self.allow_discussion_section(obj=kwargs.get("object"))
        context["app_name"] = resolve(self.request.path_info).app_name
        context["edit_url"] = reverse(f"{context['app_name']}:edit", kwargs={"uuid": self.kwargs.get("uuid")})
        context["sidebar_components"] = self.sidebar_components
        return context

    def has_edit_permission(self):
        # check if user is logged in
        if not self.request.user.is_authenticated:
            return False
        return self.get_object().is_contributor(self.request.user)

    def resolve_menu_urls(self):
        """The menu item urls generated during the plugin registration process are not resolved until this method is called."""
        if not self.menu:
            raise NotImplementedError("You must define a menu attribute on the view.")
        for item in self.menu:
            item.resolved = reverse(item.url, kwargs={"uuid": self.kwargs.get("uuid")})
        return self.menu

    def resolve_action_urls(self):
        """The action item urls generated during the plugin registration process are not resolved until this method is called."""
        for item in self.actions:
            item.resolved = reverse(item.url, kwargs={"uuid": self.kwargs.get("uuid")})

        return self.actions

    def allow_discussion_section(self, obj=None):
        """Override this method to determine whether the discussion section should be displayed based on the current object."""
        return self.allow_discussion


# @method_decorator(cache_page(60 * 5), name="dispatch")
class BaseFormView(MetadataMixin, LoginRequiredMixin, HTMXMixin, UpdateView):
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
    base_template = "geoluminate/base/create_view.html"
    template_name = "geoluminate/base/form_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # if self.object:
        # context["editing"] = True

        return context

    # def get_success_url(self):
    #     return self.object.get_absolute_url()
