from django.utils.translation import gettext as _

from geoluminate.contrib.core.view_mixins import ListPluginMixin
from geoluminate.utils import icon
from geoluminate.views import BaseDetailView, BaseEditView, BaseListView

from .filters import DatasetFilter
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
    filterset_class = DatasetFilter


class DatasetDetailView(BaseDetailView):
    base_template = "datasets/dataset_detail.html"
    model = Dataset
    title = _("Dataset")
    form_class = DatasetForm
    sidebar_fields = [
        "title",
        "project",
        "created",
        "modified",
    ]
    sidebar_components = [
        "core/sidebar/basic_info.html",
        "datasets/sidebar/project.html",
        "core/sidebar/keywords.html",
        "core/sidebar/status.html",
        "core/sidebar/summary.html",
    ]


class DatasetEditView(BaseEditView):
    model = Dataset
    form_class = DatasetForm
    related_name = "project"


class DatasetPlugin(ListPluginMixin):
    title = name = _("Datasets")
    icon = icon("dataset")

    def get_queryset(self, *args, **kwargs):
        return self.get_object().datasets.all()
