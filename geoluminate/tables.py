from auto_datatables.table import DataTable
from django.conf import settings
from django.core.exceptions import FieldDoesNotExist


class TableConfigMixin:
    # dom = "PfBpit"
    dom = "fBpit"
    language = {
        "search": "",
        "searchPlaceholder": "Search",
        "searchBuilder": {
            "button": "Complex Search",
        },
    }
    rowReorder = False
    colReorder = True
    stateSave = True
    buttons = [  # noqa: RUF012
        {
            "extend": "print",
            "text": "<i class='fas fa-print'></i>",
            "titleAttr": "Print",
            "autoPrint": False,
            "footer": True,
            # "tag": "a",
            "exportOptions": {"columns": ":not(.noPrint) :visible"},
            "messageBottom": "This is a custom message added to the print view",
        },
        {
            "extend": "collection",
            "text": "Export",
            "buttons": [
                {"extend": "csv", "exportOptions": {"columns": ":not(.noPrint) :visible"}},
                {"extend": "excel", "exportOptions": {"columns": ":not(.noPrint) :visible"}},
                {"extend": "pdf", "exportOptions": {"columns": ":not(.noPrint) :visible"}},
            ],
        },
        {
            "extend": "colvis",
            "text": "Columns",
            "collectionLayout": "fixed columns",
            # "collectionLayout": "modal",
            # "collectionTitle": "Column visibility control",
            "columns": ":not(.noVis)",
        },
        # {"extend": "searchBuilder", "config": {"depthLimit": 2}},
        # "createState",
    ]
    searchPanes = {  # noqa: RUF012
        "threshold": 0.5,
        "layout": "columns-1",
        "cascadePanes": False,
        "orderable": False,
        "dtOpts": {
            "searching": False,
            "pagingType": "numbers",
            "paging": True,
        },
    }

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class ClientSideProcessing(TableConfigMixin):
    pass


class ServerSideProcessing(TableConfigMixin):
    serverSide = True
    scrollX = True
    scrollY = "100px"


class ScrollerTable(TableConfigMixin):
    serverSide = True
    scroller = True
    scrollY = "100vh"
    scrollX = True


class GeoluminateTable(DataTable):
    uuid_template = '<span class="text-nowrap">${data}</span>'
    web_url_template = '<a href="${data}" class="btn btn-sm btn-primary">View</a>'

    debug = settings.DEBUG

    layout_overrides = {  # noqa: RUF012
        "B": ".page-header .toolbar-left",
        "i": ".footer-left",
        # "P": "#filterContainer .sidebar-body",
        ".dataTables_filter input": "#searchButton",
        "p": ".footer-right",
    }

    def build_column(self, field):
        column = super().build_column(field)
        try:
            help_text = getattr(self.model._meta.get_field(field), "help_text", None)
        except FieldDoesNotExist:
            help_text = None

        if help_text:
            column["bs-title"] = help_text
            column["bs-toggle"] = "tooltip"
            column["bs-placement"] = "bottom"

        return column
