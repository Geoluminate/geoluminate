from django.db.models.base import Model as Model
from django.urls import path
from django.utils.text import slugify
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from flex_menu import MenuItem
from meta.views import MetadataMixin

from fairdm.menus import ContributorMenu, DatasetMenu, ProjectMenu, SampleMenu
from fairdm.utils.view_mixins import RelatedObjectMixin


class PluginMenuItem(MenuItem):
    template = "fairdm/menus/detail/menu.html"


class PluggableView(RelatedObjectMixin, MetadataMixin, SingleObjectTemplateResponseMixin):
    menu = None
    name = None
    menu_check = True
    base_object_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = self.menu
        return context


class PluginRegistry:
    """PluginRegistry is used to manage a registry of plugins for the detail view of a core obejct within the FairDM database. A plugin, in this context, is represented by a view class, which is a class that defines how a certain type of page or action should be displayed or handled in a web application."""

    menus = {
        "project": ProjectMenu,
        "dataset": DatasetMenu,
        "sample": SampleMenu,
        "contributor": ContributorMenu,
    }

    def __init__(self, menu=None):
        self.registry = {k: [] for k in self.menus.keys()}
        self.menu = menu

    def register(self, view_class, to: list, **kwargs):
        """Register a page view and add it as an item to the page menu."""
        view_class = type(f"{view_class.__name__}", (view_class, PluggableView), kwargs)
        for registry in to:
            self.registry[registry].append(view_class)

    def attach_menu(self, plugin, view_name, **kwargs):
        """Creates a menu item from the view class."""
        if plugin.menu:
            self.menu.append(plugin.menu)
        else:
            self.menu.append(
                PluginMenuItem(name=plugin.name, view_name=view_name, icon=plugin.icon, check=plugin.menu_check)
            )

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
