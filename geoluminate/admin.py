from cms.models import Page
from django.conf import settings
from django.contrib import admin
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _

from .utils import get_measurement_models

# auto-register mesaurement models with Django admin
for model in get_measurement_models():
    opts = {"list_filter": []}

    # define list filters by field that have a choices attr
    for field in model._meta.get_fields():
        if hasattr(field, "choices"):
            if field.choices:
                opts["list_filter"].append(field.name)

    admin.site.register(model, **opts)


def admin_measurement_view(request):
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
