from drf_auto_endpoint.adapters import GETTER
from drf_auto_endpoint.metadata import AutoMetadata

from .adapters import DataTablesAdapter


class DatatablesAutoMetadata(AutoMetadata):
    adapter = DataTablesAdapter

    def root_metadata(self, metadata, view):
        return metadata

    def determine_metadata(self, request, view):
        metadata = {}
        endpoint = view.endpoint
        adapter = self.adapter()
        for meta_info in adapter.metadata_info:
            if meta_info.attr_type == GETTER:
                method_name = f"get_{meta_info.attr}"
                if not hasattr(endpoint, method_name):
                    metadata[meta_info.attr] = meta_info.default
                    continue
                method = getattr(endpoint, method_name)
                try:
                    metadata[meta_info.attr] = method(request)
                except TypeError:
                    metadata[meta_info.attr] = method()
            elif hasattr(endpoint, meta_info.attr):
                metadata[meta_info.attr] = getattr(endpoint, meta_info.attr, meta_info.default)
            else:
                metadata[meta_info.attr] = meta_info.default

        return adapter(metadata)
