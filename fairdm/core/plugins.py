from django.utils.translation import gettext as _

from fairdm import plugins
from fairdm.utils.utils import feature_is_enabled
from fairdm.views import FairDMListView

from .models import Dataset, Project
from .views import DataTableView


@plugins.register(to=["contributor"])
class ProjectPlugin(FairDMListView):
    """
    A plugin for displaying and filtering a list of projects related to a contributor.

    Inherits from `FairDMListView` to add filtering functionality to the list of projects.
    This plugin handles the display and filtering of projects associated with the current
    contributor.

    Behavior:
    - Registers itself to the "contributor" detail view.
    - Retrieves the list of projects associated with the contributor.
    - Supports filtering and pagination for the project list via `FairDMListView`.
    """

    title = name = _("Projects")
    icon = "project"
    model = Project

    def get_queryset(self, *args, **kwargs):
        return self.base_object.projects.all()


@plugins.register(to=["project", "contributor"])
class DatasetPlugin(FairDMListView):
    """
    A plugin for displaying and filtering datasets related to another entry in the database.

    Behavior:
    - Registers itself for both the "project" and "contributor" contexts.
    - Supports filtering and pagination for the dataset list via `FairDMListView`.
    """

    title = name = _("Datasets")
    icon = "dataset"
    model = Dataset

    def get_queryset(self, *args, **kwargs):
        return self.base_object.datasets.all()


@plugins.register(to=["dataset"])
class DataTablePlugin(DataTableView):
    title = name = _("Data")
    menu_check = feature_is_enabled("SHOW_DATA_TABLES")
    icon = "sample"
    extra_context = {
        # DANGER: REMOVE ME
        "can_add": True,
    }

    def get_queryset(self, *args, **kwargs):
        # return self.base_object.samples.instance_of(self.model)
        if hasattr(self.model, "sample_ptr"):
            return self.model.objects.filter(dataset=self.base_object)
        elif hasattr(self.model, "measurement_ptr"):
            return self.model.objects.filter(sample__dataset=self.base_object)

        return super().get_queryset(*args, **kwargs)

        # return self.model.objects.filter(dataset=self.base_object)
