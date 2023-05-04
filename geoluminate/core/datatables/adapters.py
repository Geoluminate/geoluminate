from drf_auto_endpoint.adapters import GETTER, PROPERTY, BaseAdapter, MetaDataInfo


class DataTablesAdapter(BaseAdapter):
    """
    A custom `drf_auto_endpoint.adapters` adapter that formats OPTIONS
    requests in an appropriate format for datatables.js. E.g.

    .. code:: python

        [
            {
                "data": "test",
                "title": "Test",
                "className": ,
                "defaultContent",
                "name": ,
                "orderable": ,
                "searchable": ,
                "type": ,
                "visible": ,
            },
        ]
    """

    metadata_info = [
        MetaDataInfo("columns", GETTER, []),
        MetaDataInfo("page_size", PROPERTY, 50),
        MetaDataInfo("order", GETTER, []),
        MetaDataInfo("datatables", PROPERTY, {}),
    ]

    def render(self, config):
        config.update(**config.pop("datatables"))
        return config
