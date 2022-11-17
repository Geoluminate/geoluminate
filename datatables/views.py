from django.urls import reverse
from django.views.generic import TemplateView
from drf_auto_endpoint.router import router, register
from drf_auto_endpoint.endpoints import Endpoint
from rest_framework.viewsets import ReadOnlyModelViewSet
from .renderers import DatatablesORJSONRenderer
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework_datatables_editor import pagination, filters
from rest_framework.response import Response
from .metadata import DatatablesAutoMetadata


class BaseViewSet(ReadOnlyModelViewSet):
    renderer_classes = [
        DatatablesORJSONRenderer,
        BrowsableAPIRenderer]
    metadata_class = DatatablesAutoMetadata
    filter_backends = [filters.DatatablesFilterBackend]


class DatatablesMixin(Endpoint):
    pagination_class = pagination.DatatablesPageNumberPagination
    base_viewset = BaseViewSet
    base_readonly_viewset = BaseViewSet
    invisible_fields = ()
    class_names = {}
    read_only = True
    rowId = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['remote_url'] = reverse(self.remote_url())
        return context

    def remote_url(self):
        return f"{self.get_url()}-list"

    def get_columns(self):

        columns = []

        for field in self.get_fields():
            key = field['key']
            new_field = {
                "data": key,
                "title": field.get('ui', {}).get('label', ''),
                'orderable': self.key_in(key, self.get_sortable_by()),
                "searchable": self.key_in(key, self.get_search_fields()),
                "visible": not self.key_in(key, self.invisible_fields),
            }

            if field.get('default'):
                new_field['defaultContent'] = field['default']

            if key in self.class_names.keys():
                new_field['className'] = self.class_names[key]

            columns.append(new_field)
        return columns

    def key_in(self, key, iter):
        if key in iter:
            return True
        else:
            return False

    def get_sortable_by(self):
        return self.get_iter_or_excludes('sortable_by')

    def get_search_fields(self, check_viewset_if_none=True):
        fields = super().get_search_fields(check_viewset_if_none)
        if not fields:
            fields = self.get_iter_or_excludes('search_fields', fields)
        return fields

    def get_iter_or_excludes(self, name, return_all_if_missing=True):
        include = getattr(self, name)
        exclude = getattr(self, name + '_excludes', False)
        if include:
            return include
        elif exclude:
            return [f for f in self.fields if f not in exclude]
        if return_all_if_missing:
            return self.fields

    def get_order(self):
        order_fields = self.get_ordering_fields()
        dt_order = []
        for f in order_fields:
            idx = self.fields.index(f.strip('-'))
            if f.startswith('-'):
                dt_order.append((idx, 'desc'))
            else:
                dt_order.append((idx, 'asc'))

        return dt_order


class DatatablesReadOnlyView(DatatablesMixin, TemplateView):
    template_name = 'datatables/table.html'
