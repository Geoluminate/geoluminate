from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import include, path, reverse
from django.utils.translation import gettext_lazy as _
from literature.forms import LiteratureForm
from literature.models import Literature

from geoluminate.views import BaseCreateView, BaseDetailView, BaseListView

from .filters import DatasetFilter
from .forms import DatasetForm
from .models import Dataset


class DatasetCreateView(BaseCreateView):
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


class LiteratureListView(BaseListView):
    model = Literature
    queryset = Literature.objects.all().order_by("-created")

    filterset_class = DatasetFilter


class LiteratureDetailView(BaseDetailView):
    model = Literature
    # queryset = Project.objects.all().order_by("-created")
    form_class = LiteratureForm
    # template_name = "contributors/contributor_form.html"

    def get_queryset(self):
        return super().get_queryset().order_by("-created")

    def has_edit_permission(self):
        """TODO: Add permissions."""
        # return self.request.user.is_superuser
        return None


class AddLiteratureView(BaseCreateView):
    model = Literature
    title = _("Create a new project")
    help_text = None
    form_class = LiteratureForm
