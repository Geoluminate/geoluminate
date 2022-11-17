from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework_datatables_editor.viewsets import EditorModelMixin
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


class DjangoFilterBackend(DjangoFilterBackend):

    def to_html(self, request, queryset, view):
        return ""


class BrowsableAPIRendererWithoutForms(BrowsableAPIRenderer):
    """Renders the browsable api, but excludes the forms."""

    def get_rendered_html_form(self, data, view, method, request):
        return None

    def get_filter_form(self, data, view, request):
        return None


class DatatablesReadOnlyModelViewSet(
        EditorModelMixin, viewsets.ReadOnlyModelViewSet):
    pass
