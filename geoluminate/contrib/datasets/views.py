from django.utils.translation import gettext_lazy as _

from geoluminate.views import BaseDetailView, BaseFormView, BaseListView

from .filters import DatasetFilter
from .forms import DatasetForm
from .models import Dataset


class DatasetCreateView(BaseFormView):
    model = Dataset
    title = _("Create a new dataset")
    help_text = None
    form_class = DatasetForm


class DatasetListView(BaseListView):
    template_name = "datasets/dataset_list.html"
    model = Dataset
    queryset = Dataset.objects.prefetch_related("contributors").order_by("-created")
    filterset_class = DatasetFilter


class DatasetDetailView(BaseDetailView):
    model = Dataset
    form_class = DatasetForm

    def get_context_data(self, **kwargs):
        print(self.request.htmx)
        return super().get_context_data(**kwargs)


class DatasetFormView(BaseFormView):
    model = Dataset
    form_class = DatasetForm
    template_name = "contributors/contributor_form.html"
