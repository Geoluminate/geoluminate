from django.utils.translation import gettext as _
from literature.models import LiteratureItem

from geoluminate.views import BaseListView


class ReferenceListView(BaseListView):
    title = _("References")
    model = LiteratureItem
    template_name = "geoluminate/base/list_view.html"
    queryset = LiteratureItem.objects.all()
    filterset_fields = [
        "title",
    ]


# class DatasetDetailView(BaseDetailView):
#     base_template = "datasets/dataset_detail.html"
#     model = Dataset
#     title = _("Dataset")
#     extra_context = {
#         "menu": "DatasetDetailMenu",
#         "sidebar_fields": [
#             "title",
#             "project",
#             "created",
#             "modified",
#         ],
#     }


# class DatasetEditView(BaseEditView):
#     model = Dataset
#     form_class = DatasetForm
#     related_name = "project"


# class DatasetPlugin(ListPluginMixin):
#     title = name = _("Datasets")
#     icon = "dataset"

#     def get_queryset(self, *args, **kwargs):
#         return self.base_object.datasets.all()
