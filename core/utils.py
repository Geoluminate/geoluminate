from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework_datatables_editor.viewsets import EditorModelMixin
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
import importlib

def get_choices(model, field):
    return [(k, k) for k in model.objects.order_by(field).values_list(field, flat=True).distinct()]

def import_attribute(path):
    assert isinstance(path, str)
    pkg, attr = path.rsplit(".", 1)
    ret = getattr(importlib.import_module(pkg), attr)
    return ret

def get_form_class(forms, form_id, default_form):
    form_class = forms.get(form_id, default_form)
    if isinstance(form_class, str):
        form_class = import_attribute(form_class)
    return form_class



class DjangoFilterBackend(DjangoFilterBackend):

    def to_html(self, request, queryset, view):
        return ""

class BrowsableAPIRendererWithoutForms(BrowsableAPIRenderer):
    """Renders the browsable api, but excludes the forms."""
    def get_rendered_html_form(self, data, view, method, request):
        return None

    def get_filter_form(self, data, view, request):
        return None

class DatatablesReadOnlyModelViewSet(EditorModelMixin, viewsets.ReadOnlyModelViewSet):
    pass