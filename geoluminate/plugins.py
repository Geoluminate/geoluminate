from django.urls import path
from django.utils.text import slugify
from flex_menu import MenuItem

from geoluminate.contrib.contributors.views import ContributorDetailView
from geoluminate.contrib.datasets.views import DatasetDetailView
from geoluminate.contrib.projects.views import ProjectDetailView
from geoluminate.contrib.samples.views import SampleDetailView
from geoluminate.menus import ContributorDetailMenu, DatasetDetailMenu, ProjectDetailMenu, SampleDetailMenu


class PluginRegistry:
    """PluginRegistry is used to manage a registry of plugins for the detail view of a core obejct within the Geoluminate database. A plugin, in this context, is represented by a view class, which is a class that defines how a certain type of page or action should be displayed or handled in a web application."""

    def __init__(self, base=None, menu=None):
        self.base = base
        self.registry = []
        self.menu = menu
        self.model_name = self.base.model._meta.model_name
        # self.urls = []

    def append_to_registry(self, view_class, name="", **kwargs):
        """Append a view to the registry."""
        name = slugify(name)
        view_name = f"{self.model_name}-{name}"
        self.registry.append(
            {
                "name": name,
                "route": f"{name}/",
                "view_class": view_class,
                "view_name": view_name,
                "kwargs": kwargs,
            }
        )
        return view_name

    def append_to_urls(self, view_class, name, **kwargs):
        """Append a view to the urls."""
        name = slugify(name)
        view_name = f"{self.model_name}-{name}"
        self.urls.append(path(f"{name}/", view_class.as_view(base=self.base, **kwargs), name=view_name))
        return view_name

    def register_page(self, view_class, name="", *args, **kwargs):
        """Register a page view and add it as an item to the page menu."""
        view_class = type(f"{view_class.__name__}Plugin", (view_class, self.base), {})
        name = name or getattr(view_class, "name", None)
        view_name = self.append_to_registry(view_class, name, **kwargs)
        # self.append_to_urls(view_class, name, **kwargs)
        self.build_menu_item(view_class, view_name, name, **kwargs)

    def page(self, *args, **kwargs):
        """Decorator to register a page view and add it as an item to the page menu.

        Usage:

        @dataset.page("overview", icon="fas fa-book-open")
        class SomeView(BaseAppView, TemplateView):
            template_name = "some_template.html"
        """

        def decorator(view_class):
            self.register_page(view_class, *args, **kwargs)
            return view_class

        return decorator

    def build_menu_item(self, view_class, view_name, name=None, **kwargs):
        """Creates a menu item from the view class."""
        name = name or getattr(view_class, "name", None)
        self.menu.append(
            MenuItem(
                name=kwargs.get("title", name),
                view_name=view_name,
                icon=kwargs.get("icon", getattr(view_class, "icon", None)),
                # check=lambda request: view_class.has_permission(request),
            )
        )

    def get_urls(self):
        urls = []
        for i, plugin in enumerate(self.registry):
            view_kwargs = plugin["kwargs"].get("view_kwargs", {})
            view = plugin["view_class"].as_view(**view_kwargs)
            # duplicate the first plugin with a blank route to use as the default view
            if i == 0:
                urls.append(path("", view, name=f"{self.model_name}-detail"))
            urls.append(path(plugin["route"], view, name=plugin["view_name"]))
        return urls

    @property
    def urls(self):
        if not hasattr(self, "_urls"):
            self._urls = self.get_urls()
        return self._urls


project = PluginRegistry(base=ProjectDetailView, menu=ProjectDetailMenu)

dataset = PluginRegistry(base=DatasetDetailView, menu=DatasetDetailMenu)

sample = PluginRegistry(base=SampleDetailView, menu=SampleDetailMenu)

contributor = PluginRegistry(base=ContributorDetailView, menu=ContributorDetailMenu)
