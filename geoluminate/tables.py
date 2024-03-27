from auto_datatables.table import DataTable
from django.conf import settings
from django.core.exceptions import FieldDoesNotExist


class TableConfigMixin:
    language = {
        "search": "",
        "searchPlaceholder": "Search",
        "searchBuilder": {
            "button": "Complex Search",
        },
    }
    colReorder = True
    stateSave = True
    fixedColumns = {"start": 3}
    buttons = [
        {
            "extend": "print",
            "titleAttr": "Print",
            "footer": True,
            "exportOptions": {"columns": ":not(.noPrint) :visible"},
            # "messageBottom": "This is a custom message added to the print view",
        },
        # {
        #     "extend": "collection",
        #     "text": "Export",
        #     "buttons": [
        #         {"extend": "csv", "exportOptions": {"columns": ":not(.noPrint) :visible"}},
        #         {"extend": "excel", "exportOptions": {"columns": ":not(.noPrint) :visible"}},
        #         {"extend": "pdf", "exportOptions": {"columns": ":not(.noPrint) :visible"}},
        #     ],
        # },
        "colvis",
        "searchPanes",
        "searchBuilder",
        # "createState",
        # {
        #     "extend": "createState",
        #     "text": "<i class='fa-solid fa-floppy-disk'></i>",
        # },
    ]
    searchPanes = {
        # "threshold": 0.5,
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
    processing = True
    # serverSide = True
    fixedHeader = True
    scrollCollapse = False
    scroller = True
    # scroller = {"loadingIndicator": True, "serverWait": 500}
    scrollX = False


class GeoluminateTable(DataTable):
    uuid_template = '<span class="text-nowrap">${data}</span>'
    details_template = '<a href="${data}" class="btn btn-sm btn-primary">View</a>'
    foreignkey_widget_template = '<a href="${data}" class="btn btn-sm btn-primary">View</a>'
    debug = settings.DEBUG

    def build_column(self, field):
        column = super().build_column(field)
        is_numeric = False
        try:
            model_field = self.model._meta.get_field(field)
            help_text = getattr(model_field, "help_text", None)
            is_numeric = model_field.get_internal_type() in [
                "IntegerField",
                "FloatField",
                "DecimalField",
            ]
        except FieldDoesNotExist:
            help_text = None

        if help_text:
            column["bs-title"] = help_text
            column["bs-toggle"] = "tooltip"
            column["bs-placement"] = "bottom"

        if is_numeric:
            column["class"] = "text-center"
        return column
