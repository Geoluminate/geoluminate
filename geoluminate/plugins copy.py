from django.apps import apps
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import path
from django.utils.text import slugify
from flex_menu import MenuItem

from geoluminate.contrib.contributors.views import ContributorDetailView
from geoluminate.contrib.datasets.views import DatasetDetailView
from geoluminate.contrib.projects.views import ProjectDetailView
from geoluminate.contrib.samples.views import SampleDetailView
from geoluminate.menus import ContributorDetailMenu, DatasetDetailMenu, ProjectDetailMenu, SampleDetailMenu


class BasePlugin:
    core_mapping = {
        "p": "projects.Project",
        "d": "datasets.Dataset",
        "s": "samples.Sample",
        "m": "measurements.Measurement",
        "c": "contributors.Contributor",
    }

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        mtype = self.core_mapping.get(pk[0], None)
        if not mtype:
            raise Http404("Object does not exist")
        self.base_model = apps.get_model(mtype)
        self.base_object = get_object_or_404(self.base_model, pk=pk)
        if hasattr(self.base_object, "polymorphic_model_marker"):
            pass
            # self.base_model = self.related_object.polymorphic_model_marker

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["base_model"] = self.base_model
        context["base_model_name"] = self.base_model._meta.verbose_name
        context["base_model_name_plural"] = self.base_model._meta.verbose_name_plural
        context["base_object"] = self.base_object
        context[self.base_model._meta.model_name] = self.base_object
        return context


class PluginRegistry:
    """PluginRegistry is used to manage a registry of plugins for the detail view of a core obejct within the Geoluminate database. A plugin, in this context, is represented by a view class, which is a class that defines how a certain type of page or action should be displayed or handled in a web application.

    The PluginRegistry class has several attributes: namespace, registry, menu, and actions. The namespace is the name of the application the plugins are registered to. The registry is a list that stores all registered plugins. The menu and actions are lists that store menu items and actions respectively.

    The append_to_registry method is used to add a new plugin to the registry. It takes a view class and some optional parameters, generates a name and route for the view, and appends a dictionary with these details to the registry.

    The register_page and register_action methods are used to register a page view or an action view respectively. They call append_to_registry to add the view to the registry, and then add a menu item or an action item to the menu or actions list.

    The page and action methods are decorators that can be used to register a page view or an action view. They call register_page or register_action respectively.

    The build_menu_item method is used to create a menu item from a view class. It returns an instance of MenuItem with the details of the menu item.

    The get_urls method is used to generate a list of URL patterns for all registered plugins. It iterates over the registry, creates a view for each plugin, and appends a URL pattern for the view to the list of URLs.

    The urls property is a cached property that returns the list of URL patterns. It calls get_urls the first time it's accessed, and then stores the result for future accesses.

    """

    def __init__(self, namespace="", base=None, menu=None):
        self.namespace = namespace
        self.base = base
        self.registry = []
        self.menu = menu
        self.model_name = self.base.model._meta.model_name

    def append_to_registry(self, view_class, name="", *args, **kwargs):
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

    def register_page(self, view_class, name="", *args, **kwargs):
        """Register a page view and add it as an item to the page menu."""
        bases = kwargs.get("bases", [])
        if not isinstance(bases, list):
            bases = [bases]
        # view_class = type(f"{view_class.__name__}Plugin", (view_class, *bases, self.base), {})
        view_class = type(
            f"{view_class.__name__}Plugin",
            (
                view_class,
                *bases,
            ),
            {},
        )
        name = name or getattr(view_class, "name", None)
        view_name = self.append_to_registry(view_class, name, *args, **kwargs)
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
            # view = plugin["view_class"].as_view(base=self.base, **view_kwargs)
            view = plugin["view_class"].as_view(**view_kwargs)
            if i == 0:
                # duplicate the first plugin with a blank route to use as the default view
                urls.append(path("", view, name=f"{self.model_name}-detail"))
            # append the plugin with the route
            if plugin["route"] == "/":
                print(self.namespace, plugin["view_class"])

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
