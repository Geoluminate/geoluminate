from drf_orjson_renderer.renderers import ORJSONRenderer


class DatatablesORJSONRenderer(ORJSONRenderer):
    """This class is an integration of
    drf_orjson_renderer.renderers.ORJSONRenderer and
    rest_framework_datatables_editor.renderers.DatatablesRenderer.
    It provides
    the correct format for datatables with the speed of ORJSON."""

    format: str = "datatables"
    html_media_type: str = "text/html"
    json_media_type: str = "application/json"
    media_type: str = json_media_type

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into JSON, returning a bytestring.
        """
        if data is None:
            return b""

        request = renderer_context["request"]

        if request.method == "OPTIONS":
            return super().render(data, accepted_media_type, renderer_context)

        new_data = {}

        view = renderer_context.get("view")

        if "recordsTotal" not in data:
            # pagination was not used, let's fix the data dict
            if "results" in data:
                results = data["results"]
                count = data["count"] if "count" in data else len(results)
            else:
                results = data
                count = len(results)
            # new_data['data'] = results
            if view and hasattr(view, "_datatables_filtered_count"):
                count = view._datatables_filtered_count
            total_count = view._datatables_total_count if view and hasattr(view, "_datatables_total_count") else count
            new_data["draw"] = int(request.query_params.get("draw", "1"))
            new_data["recordsFiltered"] = count
            new_data["recordsTotal"] = total_count
            new_data["data"] = results
        else:
            new_data = data
            # add datatables "draw" parameter
            new_data["draw"] = int(request.query_params.get("draw", "1"))

        serializer_class = None
        if hasattr(view, "get_serializer_class"):
            serializer_class = view.get_serializer_class()
        elif hasattr(view, "serializer_class"):
            serializer_class = view.serializer_class

        if serializer_class is not None and hasattr(serializer_class, "Meta"):
            force_serialize = getattr(serializer_class.Meta, "datatables_always_serialize", ())
        else:
            force_serialize = ()

        self._filter_unused_fields(request, new_data, force_serialize)

        if hasattr(view.__class__, "Meta"):
            extra_json_funcs = getattr(view.__class__.Meta, "datatables_extra_json", ())
        else:
            extra_json_funcs = ()

        self._filter_extra_json(view, new_data, extra_json_funcs)

        return super().render(new_data, accepted_media_type, renderer_context)

    def _filter_unused_fields(self, request, result, force_serialize):
        # list of params to keep, triggered by ?keep= and can be comma
        # separated.
        keep = request.query_params.get("keep", [])
        cols = []
        i = 0
        while True:
            col = request.query_params.get("columns[%d][data]" % i)
            if col is None:
                break
            cols.append(col.split(".").pop(0))
            i += 1
        if len(cols):
            data = result["data"]
            for i, item in enumerate(data):
                try:
                    keys = set(item.keys())
                except AttributeError:
                    continue
                for k in keys:
                    if k not in cols and not k.startswith("DT_Row") and k not in force_serialize and k not in keep:
                        result["data"][i].pop(k)

    def _filter_extra_json(self, view, result, extra_json_funcs):
        read_only_keys = result.keys()  # don't alter anything
        for func in extra_json_funcs:
            if not hasattr(view, func):
                raise TypeError(f"extra_json_funcs: {func} not a view method.")
            method = getattr(view, func)
            if not callable(method):
                raise TypeError(f"extra_json_funcs: {func} not callable.")
            key, val = method()
            if key in read_only_keys:
                raise ValueError(f"Duplicate key found: {key}")
            result[key] = val
