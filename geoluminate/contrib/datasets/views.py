from django.utils.translation import gettext as _

from geoluminate.contrib.core.view_mixins import ListPluginMixin
from geoluminate.utils import icon
from geoluminate.views import (
    BaseDetailView,
    BaseFormView,
    BaseListView,
)

from .filters import DatasetFilter
from .forms import DatasetForm
from .models import Dataset


class DatasetCreateView(BaseFormView):
    """
    A Django class-based view for creating a new Dataset instance.

    This view inherits from `BaseFormView` and sets several attributes:
    - model: The model class that this view will create instances of. In this case, it's `Dataset`.
    - description: The title that will be displayed on the page. In this case, it's "Create a new dataset".
    - form_class: The form class that will be used for creating the new `Dataset` instance. In this case, it's `DatasetForm`.

    When a GET request is made to this view, it will render a form for creating a new `Dataset` instance.
    When a POST request is made to this view, it will validate the form and, if the form is valid, create a new `Dataset` instance.
    """

    model = Dataset
    title = _("Create a new dataset")
    description = None
    form_class = DatasetForm


class DatasetListView(BaseListView):
    """
    A Django class-based view for displaying a list of Dataset instances.

    This view inherits from `BaseListView` and sets several attributes:
    - template_name: The name of the template that will be used to render the view. In this case, it's "datasets/dataset_list.html".
    - model: The model class that this view will display instances of. In this case, it's `Dataset`.
    - queryset: The Django QuerySet that defines the list of instances that this view will display. In this case, it's all `Dataset` instances, ordered by the `created` field in descending order, with related `contributors` instances prefetched.
    - filterset_class: The class that will be used to filter the instances that this view will display. In this case, it's `DatasetFilter`.

    When a GET request is made to this view, it will render a list of `Dataset` instances, filtered according to the `DatasetFilter` class and ordered by the `created` field in descending order.
    """

    title = _("Datasets")
    base_template = "datasets/dataset_list.html"
    object_template = "datasets/dataset_card.html"
    model = Dataset
    queryset = Dataset.objects.prefetch_related("contributors").order_by("-created")
    filterset_class = DatasetFilter


class DatasetDetailView(BaseDetailView):
    base_template = "datasets/dataset_detail.html"
    model = Dataset
    title = _("Dataset")
    form_class = DatasetForm
    sidebar_components = [
        "core/sidebar/basic_info.html",
        "datasets/sidebar/project.html",
        "core/sidebar/keywords.html",
        "core/sidebar/status.html",
        "core/sidebar/summary.html",
    ]


class DatasetFormView(BaseFormView):
    model = Dataset
    form_class = DatasetForm
    template_name = "contributors/contributor_form.html"


class DatasetPlugin(ListPluginMixin):
    template_name = "geoluminate/plugins/base_list.html"
    object_template = "datasets/dataset_card.html"
    title = name = _("Datasets")
    icon = icon("dataset")
    description = _("The following datasets are associated with the this project.")

    def get_queryset(self, *args, **kwargs):
        return self.get_object().datasets.all()
