from django.apps import apps
from django.db.models.base import Model as Model
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import path
from django.utils.text import slugify
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from flex_menu import MenuItem
from meta.views import MetadataMixin

from geoluminate.contrib import CORE_MAPPING
from geoluminate.core.views.mixins import HTMXMixin
from geoluminate.menus import ContributorMenu, DatasetMenu, OrganizationMenu, ProjectMenu, SampleMenu


class PluggableView(MetadataMixin, HTMXMixin, SingleObjectTemplateResponseMixin):
    menu = None
    name = None

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        if mtype := CORE_MAPPING.get(pk[0], None):
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
        context["menu"] = self.menu
        return context


class PluginRegistry:
    """PluginRegistry is used to manage a registry of plugins for the detail view of a core obejct within the Geoluminate database. A plugin, in this context, is represented by a view class, which is a class that defines how a certain type of page or action should be displayed or handled in a web application."""

    # registry = {
    #     "project": [],
    #     "dataset": [],
    #     "sample": [],
    #     "person": [],
    #     "organization": [],
    # }
    menus = {
        "project": ProjectMenu,
        "dataset": DatasetMenu,
        "sample": SampleMenu,
        "person": ContributorMenu,
        "organization": OrganizationMenu,
    }

    def __init__(self, menu=None):
        self.registry = {k: [] for k in self.menus.keys()}
        self.menu = menu

    def register(self, view_class, to: list, **kwargs):
        """Register a page view and add it as an item to the page menu."""
        view_class = type(f"{view_class.__name__}", (view_class, PluggableView), kwargs)
        for registry in to:
            self.registry[registry].append(view_class)
        # self.registry.append(type(f"{view_class.__name__}", (view_class, PluggableView), kwargs))

    def attach_menu(self, plugin, view_name, **kwargs):
        """Creates a menu item from the view class."""
        if plugin.menu:
            self.menu.append(plugin.menu)
        else:
            self.menu.append(MenuItem(name=plugin.name, view_name=view_name, icon=plugin.icon))

    def get_urls(self, registry_name):
        urls = []
        self.menu = self.menus[registry_name]
        for plugin in self.registry[registry_name]:
            url_base = slugify(plugin.name)
            view_name = f"{registry_name}-{url_base}"
            self.attach_menu(plugin, view_name)
            urls.append(path(f"{url_base}/", plugin.as_view(menu=self.menu), name=view_name))
        return urls


plugins = PluginRegistry()


def register(to, **kwargs):
    """Decorator to register a page view and add it as an item to the page menu."""

    def decorator(view_class):
        plugins.register(view_class, to, **kwargs)
        return view_class

    return decorator
