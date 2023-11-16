from django.urls import path
from django.utils.text import slugify
from simple_menu import MenuItem


class PluginRegistry:
    def __init__(self, app_name=""):
        self.app_name = app_name
        self.registry = []
        self.menu = []
        self.actions = []

    def append_to_registry(self, view_class, name="", route="", **kwargs):
        """Append a view to the registry."""
        # print(view_class.__name__)
        view_name = view_class.__name__.lower()
        if view_class.model:
            model_name = view_class.model._meta.model_name
            name = slugify(f"{model_name}-{view_name}")
        else:
            name = slugify(view_name)
        route = route or f"{name}/"
        self.registry.append(
            {
                "name": name,
                "route": slugify(route),
                "view_class": view_class,
                "view_name": f"{self.app_name}:{name}" if self.app_name else name,
                "kwargs": kwargs,
            }
        )
        return f"{self.app_name}:{name}" if self.app_name else name

    def register_page(self, view_class, name="", route="", **kwargs):
        """Register a page view and add it as an item to the page menu."""
        view_name = self.append_to_registry(view_class, name, route, **kwargs)
        self.menu.append(self.build_menu_item(view_class, name, view_name, **kwargs))

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

    def register_action(self, view_class, name="", route="", **kwargs):
        """Register an action view and add it as an item to the action menu."""
        view_name = self.append_to_registry(view_class, name, route, **kwargs)
        self.actions.append(self.build_menu_item(view_class, name, view_name, **kwargs))

    def build_menu_item(self, view_class, name, view_name, **kwargs):
        """Creates a menu item from the view class."""
        return MenuItem(
            title=kwargs.get("title", name),
            url=view_name,
            icon=kwargs.get("icon"),
            check=lambda request: view_class.has_permission(request),
            hx={"hx-target": "#main-content"},
        )

    def action(self, *args, **kwargs):
        """Decorator to register an action view and add it as an item to the action menu.

        Usage:

        @dataset.action("download", icon="fas fa-file-download")
        class DownloadView(BaseAppView, DatasetDetailView):
            def get_file(self):
                obj = self.get_object()
                return ContentFile(obj.generate_xml(), name=f"{slugify(obj.title)}.xml")
        """

        def decorator(view_class):
            self.register_action(view_class, *args, **kwargs)
            return view_class

        return decorator

    def get_urls(self):
        urls = []
        for i, plugin in enumerate(self.registry):
            view_kwargs = plugin["kwargs"].get("view_kwargs", {})
            view = plugin["view_class"].as_view(menu=self.menu, actions=self.actions, **view_kwargs)
            if i == 0:
                # duplicate the first plugin with a blank route to use as the default view
                urls.append(path("", view, name="detail"))
            # append the plugin with the route
            urls.append(path(plugin["route"], view, name=plugin["name"]))
        return urls

    @property
    def urls(self):
        if not hasattr(self, "_urls"):
            self._urls = self.get_urls()
        return self._urls


project = PluginRegistry("projects")
dataset = PluginRegistry("datasets")
sample = PluginRegistry("samples")
contributor = PluginRegistry("contributor")
location = PluginRegistry("locations")
review = PluginRegistry("reviews")
