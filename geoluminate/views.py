from django.conf import settings
from django.http import JsonResponse
from django.utils.module_loading import import_string
from django_select2.views import AutoResponseView

# from geoluminate.conf import settings
from geoluminate.core.datatables.views import DatatablesReadOnlyView


# @datatables.register
class DatabaseTableView(DatatablesReadOnlyView):
    template_name = "geoluminate/database_table.html"
    # model = HeatFlow
    read_only = True
    search_fields = ("name",)
    invisible_fields = [
        "id",
    ]
    fields = [
        "get_absolute_url",
        "id",
        "name",
        "q_date_acq",
        "environment",
        "water_temp",
        "explo_method",
        "explo_purpose",
    ]
    invisible_fields = [
        "id",
    ]
    datatables = {
        "dom": "<'#tableToolBar' if> <'#tableBody' tr>",
        "processing": True,
        "scrollY": "100vh",
        "deferRender": True,
        "scroller": True,
        "rowId": "id",
    }


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
