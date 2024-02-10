from cms.models import Page
from django.conf import settings
from django.contrib import admin
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _

from .utils import get_measurement_models


"""
This loop iterates over each model returned by the `get_measurement_models` function.

For each model, it creates a dictionary `opts` with a key `list_filter` that maps to an empty list.
It then iterates over each field in the model's meta information. If a field has a `choices` attribute and this attribute is not empty,
the field's name is appended to the `list_filter` list in the `opts` dictionary.

Finally, the model is registered in the Django admin site with the `opts` dictionary as options.
This means that in the Django admin site, a filter will be added for each field that has choices.
"""
for model in get_measurement_models():
    
    opts = {"list_filter": []}

    # define list filters by field that have a choices attr
    for field in model._meta.get_fields():
        if hasattr(field, "choices"):
            if field.choices:
                opts["list_filter"].append(field.name)

    admin.site.register(model, **opts)


def admin_measurement_view(request):
    """
    A Django admin view that collects and displays all models admin classes that register a model that subclasses
    `geoluminate.Measurement`.

    This function retrieves a list of measurement models using the `get_measurement_models` function.
    It then gets the app labels for these models and retrieves the corresponding app lists from the admin site.
    The app lists are combined into a single list, which is included in the context data for rendering the view.

    The context data also includes the title, which is set to the acronym of the geoluminate database followed by "Measurements",
    and the app label, which is set to "geoluminate".

    The view is rendered using the `TemplateResponse` class, with the template being either "admin/{app_label}/app_index.html" or "admin/app_index.html",
    depending on whether the former exists.

    Args:
        request (django.http.HttpRequest): The HTTP request.

    Returns:
        django.template.response.TemplateResponse: The HTTP response.
    """

    measurements = get_measurement_models()

    app_labels = {model._meta.app_label for model in measurements}

    app_list = []
    for app_label in app_labels:
        app_list += admin.site.get_app_list(request, app_label)

    app_label = "geoluminate"

    context = {
        **admin.site.each_context(request),
        "title": _(f"{settings.GEOLUMINATE['database']['acronym']} Measurements"),
        "subtitle": None,
        "app_list": app_list,
        "app_label": app_label,
        # **(extra_context or {}),
    }

    # request.current_app = self.name

    return TemplateResponse(
        request,
        admin.site.app_index_template or ["admin/%s/app_index.html" % app_label, "admin/app_index.html"],
        context,
    )
