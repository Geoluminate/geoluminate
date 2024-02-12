from auto_datatables.table import DataTable
from django.conf import settings
from django.core.exceptions import FieldDoesNotExist


class TableConfigMixin:
    dom = """   
    <'page-nav'
        <'nav nav-pills nav-pills-alternate'<B><'ms-auto my-auto'f>>
    >t<'px-1 position-absolute bottom-0 end-0'i>
                """  # noqa: W291
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
        # {
        #     "extend": "print",
        #     "text": "<i class='fa-solid fa-print'></i> Print",
        #     "titleAttr": "Print",
        #     "autoPrint": False,
        #     "footer": True,
        #     "exportOptions": {"columns": ":not(.noPrint) :visible"},
        #     # "messageBottom": "This is a custom message added to the print view",
        # },
        # {
        #     "extend": "collection",
        #     "text": "<i class='fa-solid fa-file-export'></i> Export",
        #     "buttons": [
        #         {"extend": "csv", "exportOptions": {"columns": ":not(.noPrint) :visible"}},
        #         {"extend": "excel", "exportOptions": {"columns": ":not(.noPrint) :visible"}},
        #         # {"extend": "pdf", "exportOptions": {"columns": ":not(.noPrint) :visible"}},
        #     ],
        # },
        {
            "extend": "colvis",
            "text": "<i class='fa-solid fa-table-columns'></i> Columns",
            # "collectionLayout": "fixed columns",
            # "collectionLayout": "modal",
            # "collectionTitle": "Column visibility control",
            # "columns": ":not(.noVis)",
        },
        {
            "extend": "searchBuilder",
            "text": "<i class='fa-solid fa-filter'></i> Complex Search",
            # "config": {"depthLimit": 2},
        },
        {
            "extend": "createState",
            "text": "<i class='fa-solid fa-floppy-disk'></i>",
        },
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
    # searchBuilder = {
    #     "layout": "columns-1",
    #     "cascadePanes": False,
    #     "orderable": False,
    # }

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
    # scrollY = "100vh"
    scrollY = "800px"
    scrollX = True


class GeoluminateTable(DataTable):
    uuid_template = '<span class="text-nowrap">${data}</span>'
    details_template = '<a href="${data}" class="btn btn-sm btn-primary">View</a>'
    foreignkey_widget_template = '<a href="${data}" class="btn btn-sm btn-primary">View</a>'
    debug = settings.DEBUG

    # layout_overrides = {  # noqa: RUF012
    #     "B": "#tableButtons>.toolbar-left",
    #     "i": "#infoPane",
    #     # "P": "#filterContainer .sidebar-body",
    #     ".dataTables_filter input": "#tableButtons>.toolbar-right.ms-auto",
    #     # "p": ".footer-right",
    # }

    def build_column(self, field):
        column = super().build_column(field)
        is_numeric = False
        try:
            model_field = self.model._meta.get_field(field)
            help_text = getattr(model_field, "help_text", None)
            is_numeric = model_field.get_internal_type() in ["IntegerField", "FloatField", "DecimalField"]
        except FieldDoesNotExist:
            help_text = None

        if help_text:
            column["bs-title"] = help_text
            column["bs-toggle"] = "tooltip"
            column["bs-placement"] = "bottom"

        if is_numeric:
            column["class"] = "text-center"
        return column
