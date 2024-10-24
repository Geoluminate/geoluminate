from django.utils.translation import gettext as _

from geoluminate.core.views.mixins import ListPluginMixin
from geoluminate.views import BaseDetailView, BaseEditView, BaseListView

from .forms import DatasetForm
from .models import Dataset


class DatasetListView(BaseListView):
    """
    A Django class-based view for displaying a list of Dataset instances.

    This view inherits from `BaseListView` and sets several attributes:
    - queryset: The Django QuerySet that defines the list of instances that this view will display. In this case, it's all `Dataset` instances, ordered by the `created` field in descending order, with related `contributors` instances prefetched.
    - filterset_class: The class that will be used to filter the instances that this view will display. In this case, it's `DatasetFilter`.

    When a GET request is made to this view, it will render a list of `Dataset` instances, filtered according to the `DatasetFilter` class and ordered by the `created` field in descending order.
    """

    title = _("Datasets")
    queryset = Dataset.objects.prefetch_related("contributors").order_by("-created")
    # filterset_class = DatasetFilter
    model = Dataset
    filterset_fields = [
        "id",
        "title",
        "license",
    ]


class DatasetDetailView(BaseDetailView):
    base_template = "datasets/dataset_detail.html"
    model = Dataset
    title = _("Dataset")
    extra_context = {
        "menu": "DatasetDetailMenu",
        "sidebar_fields": [
            "title",
            "project",
            "created",
            "modified",
        ],
    }


class DatasetEditView(BaseEditView):
    model = Dataset
    form_class = DatasetForm
    related_name = "project"


class DatasetPlugin(ListPluginMixin):
    title = name = _("Datasets")
    icon = "dataset"

    def get_queryset(self, *args, **kwargs):
        return self.base_object.datasets.all()
