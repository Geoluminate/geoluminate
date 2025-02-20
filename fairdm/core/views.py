from functools import cached_property

from django_tables2.views import SingleTableMixin

from fairdm.contrib.import_export.utils import export_choices
from fairdm.menus import DatasetMenu, ProjectMenu, SampleMenu
from fairdm.registry import registry
from fairdm.views import BaseCRUDView, FairDMListView

from .filters import DatasetFilter, ProjectFilter
from .forms import DatasetForm, ProjectForm, SampleForm
from .models import Dataset, Project, Sample
from .utils import model_class_inheritance_to_fieldsets


class ProjectCRUDView(BaseCRUDView):
    model = Project
    form_class = ProjectForm
    menu = ProjectMenu
    filterset_class = ProjectFilter

    def get_detail_context_data(self, context):
        context["descriptions"] = self.get_object().descriptions.all()
        context["all_types"] = self.object.DESCRIPTION_TYPES.choices
        return context


class DatasetCRUDView(BaseCRUDView):
    model = Dataset
    form_class = DatasetForm
    menu = DatasetMenu
    filterset_class = DatasetFilter
    paginate_by = 10

    def get_form(self, data=None, files=None, **kwargs):
        kwargs["request"] = self.request
        return super().get_form(data, files, **kwargs)

    def get_detail_context_data(self, context):
        context["descriptions"] = self.get_object().descriptions.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.add_contributor(self.request.user, with_roles=["Creator", "ProjectMember", "ContactPerson"])
        return response


class SampleCRUDView(BaseCRUDView):
    url_base = "sample"
    form_class = SampleForm
    menu = SampleMenu
    template_name = "fairdm_core/sample_detail.html"
    # @property
    # def model(self):
    #     if sample_type := self.request.GET.get("type"):
    #         return apps.get_model(sample_type)
    #     return Sample

    def get_object(self):
        sample = Sample.objects.get(pk=self.kwargs["pk"])
        self.model = type(sample)
        return sample

    def get_detail_context_data(self, context):
        context["descriptions"] = self.get_object().descriptions.all()
        context["all_types"] = self.object.DESCRIPTION_TYPES.choices
        context["model_config"] = registry.get_model(self.model)["config"]
        # context["model_metadata"] = registry.get_model(self.model)["config"]
        return context

    def get_form_class(self):
        return registry.get_model(self.model)["config"].get_form_class()

    def get_form(self, data=None, files=None, **kwargs):
        kwargs["request"] = self.request
        if data:
            data = data.copy()
            data["type"] = self.model._meta.label
            data["_position"] = "first-child"
            data["dataset"] = self.request.GET.get("dataset")
        return super().get_form(data, files, **kwargs)

    def get_sidebar_fields(self):
        return model_class_inheritance_to_fieldsets(self.object)


class DataTableView(SingleTableMixin, FairDMListView):
    export_formats = ["csv", "xls", "xlsx", "json", "latex", "ods", "tsv", "yaml"]
    template_name_suffix = "_table"
    template_name = "fairdm/data_table.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["registry"] = registry
        context["export_choices"] = export_choices
        return context

    @cached_property
    def model(self):
        self.dtype = self.request.GET.get("type")

        if not self.dtype:
            # Default to the first registered model if no type is provided
            if not registry.all:
                raise ValueError("No models are registered in the FairDMRegistry.")
            self.meta = registry.samples[0]
            self.dtype = f"{self.meta['app_label']}.{self.meta['model']}"  # Ensures dtype is still assigned
        else:
            # Retrieve the model metadata from the registry
            result = registry.get(*self.dtype.split("."))
            if not result:
                raise ValueError(f"This data type is not supported: {self.dtype}")
            self.meta = result[0]

        return self.meta["class"]

    def get_table_class(self):
        """
        Return the class to use for the table.
        """
        config = registry.get_model(self.model)
        return config["config"].get_table_class()

    def get_table_kwargs(self):
        """
        Return the keyword arguments for instantiating the table.

        Allows passing customized arguments to the table constructor, for example,
        to remove the buttons column, you could define this method in your View::

            def get_table_kwargs(self):
                return {"exclude": ("buttons",)}
        """
        return {
            "exclude": [
                "polymorphic_ctype",
                "measurement_ptr",
                "sample_ptr",
                "options",
                "image",
                "created",
                "modified",
            ],
        }

    def get_file(self):
        """Return :class:`django.core.files.base.ContentFile` object."""
        resource_class = self.model._fairdm.config.get_resource_class()
        dataset = resource_class().export(queryset=self.get_queryset())
        self.export_type = self.request.GET.get("_export")
        return dataset.export(self.export_type)

    def get_basename(self):
        return f"{self.model._meta.verbose_name_plural}.csv"

    def get_content_type(self, file):
        """Define the MIME type for the ZIP file."""
        return "text/csv"
