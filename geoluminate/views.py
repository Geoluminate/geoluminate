from auto_datatables.mixins import AjaxMixin, ScrollerMixin
from auto_datatables.tables import BaseDataTable
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.module_loading import import_string
from django_select2.views import AutoResponseView


class ModelFieldSelect2View(AutoResponseView):
    """This is a subclass of the `django_select2.views.AutoResponseView`
    that will return distinct values of a model field using the values
    themselves as both the `id` and the `text` fields in the JSONResponse.

    E.g.
        'results': [
                {'text': "foo", 'id': "foo"}
        ],
    """

    def get(self, request, *args, **kwargs):
        self.widget = self.get_widget_or_404()
        self.term = kwargs.get("term", request.GET.get("term", ""))
        field = self.widget.search_fields[0].split("__")[0]
        self.object_list = self.get_queryset().values_list(field, flat=True).order_by(field).distinct()
        context = self.get_context_data()
        return JsonResponse(
            {
                "results": [{"text": obj, "id": obj} for obj in context["object_list"]],
                "more": context["page_obj"].has_next(),
            },
            encoder=import_string(settings.SELECT2_JSON_ENCODER),
        )


def placeholder_view(request):
    """This is a placeholder view that can be used to add dummy urls to the
    project. Use it as a placeholder to design things like toolbars, menus,
    navigation, etc. without having to worry about the underlying view."""
    return render(request, "geoluminate/placeholder.html")


class SmallTableView(AjaxMixin, BaseDataTable):
    # stateSave = True
    paging = False
    fixedHeader = True
    dom = "PBitf"
    searchPanes = {  # noqa: RUF012
        "threshold": 0.5,
        "layout": "columns-1",
        "cascadePanes": True,
        "orderable": False,
        "dtOpts": {
            "searching": True,
            "pagingType": "numbers",
            "paging": True,
        },
    }
    layout = {  # noqa: RUF012
        "B": ".application-menu .btn-toolbar .left",
        "i": "#appFooter",
        "P": "#filterContainer .offcanvas-body",
        ".dataTables_filter input": ".application-menu #searchButton",
    }


class LargeTableView(BaseDataTable, ScrollerMixin):
    # stateSave = True
    fixedHeader = True
    dom = "Bit"
    layout = {  # noqa: RUF012
        "B": ".application-menu .btn-toolbar .left",
        "i": "#appFooter",
        "P": "#filterContainer .offcanvas-body",
        ".dataTables_filter input": ".application-menu #searchButton",
    }
