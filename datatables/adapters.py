from drf_auto_endpoint.adapters import BaseAdapter, MetaDataInfo, PROPERTY, GETTER


class DataTablesAdapter(BaseAdapter):
    """
    Here is an example of the expected output
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
        MetaDataInfo('columns', GETTER, []),
        MetaDataInfo('page_size', PROPERTY, 50),
        MetaDataInfo('order', GETTER, []),
        MetaDataInfo('datatables', PROPERTY, {}),
    ]

    def render(self, config):
        config.update(**config.pop('datatables'))
        return config
