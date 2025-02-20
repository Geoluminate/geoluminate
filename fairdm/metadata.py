from dataclasses import dataclass
from typing import Any

from django.contrib.admin.utils import flatten
from django.forms import ModelForm
from django.utils.module_loading import import_string
from django_filters import FilterSet
from django_tables2 import Table, table_factory
from import_export.resources import ModelResource
from rest_framework.serializers import ModelSerializer

from fairdm.utils import factories
from fairdm.utils.utils import fairdm_fieldsets_to_django


@dataclass(frozen=True, kw_only=True)
class Authority:
    name: str
    """The name of the authority that created this metadata. This is required."""

    short_name: str = ""
    """The short name of the authority that created this metadata."""

    website: str = ""
    """The website of the authority that created this metadata."""


@dataclass(frozen=True, kw_only=True)
class Citation:
    text: str = ""
    """The citation for the data model."""

    doi: str = ""
    """The DOI for the citation."""


class ModelConfig:
    METADATA_ATTRS = [
        "description",
        "authority",
        "keywords",
        "repository_url",
        "citation",
        "maintainer",
        "maintainer_email",
    ]
    CONFIG_ATTRS = [
        "fields",
        "fieldsets",
        "form_class",
        "form_options",
        "filterset_class",
        "filterset_options",
        "table_class",
        "table_options",
        "resource_class",
        "resource_options",
        "serializer_class",
        "serializer_kwargs",
    ]

    # METADATA ATTRIBUTES
    description = None
    """A description of the data type represented by the model."""

    authority = None
    """The authority that created this metadata. This is required."""

    keywords = []
    """A list of controlled keywords that describe the data model."""

    repository_url: str = ""
    """The URL of the repository where the data model can be viewed."""

    citation = []
    """The citation for the data model."""

    maintainer: str = ""
    """The name of the package maintainer of the data model."""

    maintainer_email: str = ""
    """The email address of the package maintainer of the data model."""

    # CONFIG ATTRIBUTES
    fields = []

    private_fields = []
    """Fields that should not be displayed in forms, tables or exports."""

    fieldsets = []
    """Fieldsets to group fields in forms and detail views."""

    form_class: type[ModelForm] = ModelForm
    """The ModelForm class or path to the ModelForm class."""

    form_options: dict = {}
    """Additional keyword arguments to pass to the ModelForm class."""

    filterset_class: type[FilterSet] = FilterSet
    """A django-filter filter class to use for filtering data. If None, a filter will be generated automatically using fairdm.factories.model_filter_factory."""

    filterset_options = {}
    """A list of fields to include in the filter. If filterset_class is None, a filter will be generated automatically using fairdm.factories.model_filter_factory."""

    table_class: type[Table] = Table
    """A django-tables2 table class to use for displaying data. If None, a table will be generated automatically using fairdm.factories.model_table_factory."""

    table_options = {}
    """Additional keyword arguments to pass to the table class."""

    resource_class: type[ModelResource] = ModelResource
    """A django-import-export resource class to use for importing and exporting data. If None, a resource will be generated automatically using fairdm.factories.model_resource_factory."""

    resource_options = {}
    """When resource_class is None, the resource is generated automatically using fairdm.factories.model_resource_factory. Use this dictionary to supply Meta class options to the generated resource."""

    serializer_class: type[ModelSerializer] = ModelSerializer
    """The ModelSerializer class or path to the ModelSerializer class."""

    serializer_kwargs: dict = {}
    """Additional keyword arguments to pass to the ModelSerializer class."""

    @classmethod
    def declared_attrs(cls):
        return [
            attr for attr in dir(ModelConfig) if not callable(getattr(ModelConfig, attr)) and not attr.startswith("_")
        ]

    @classmethod
    def defaults(cls):
        return {attr: getattr(ModelConfig, attr) for attr in ModelConfig.declared_attrs()}

    @classmethod
    def as_dict(cls):
        return {attr: getattr(cls, attr) for attr in ModelConfig.declared_attrs()}

    def __init__(self, model_class: type[Any]):
        self.model = model_class

    def _get_class(self, class_or_path: str | type[Any]) -> type[Any]:
        """
        Resolves a class reference from a string path or returns the class itself.

        Args:
            class_or_path (str | Type[Any]): A class path string or a class reference.

        Returns:
            Type[Any]: The resolved class.

        Raises:
            ImportError: If the class path is invalid.
        """
        if isinstance(class_or_path, str):
            return import_string(class_or_path)
        return class_or_path

    def get_fields(self):
        if not self.fields:
            return []

        if "id" not in self.fields:
            return ["id", "dataset"] + self.fields
        return self.fields

    def get_fieldsets(self):
        if self.fieldsets and isinstance(self.fieldsets, dict):
            return fairdm_fieldsets_to_django(self.fieldsets)
        elif self.fieldsets and isinstance(self.fieldsets, list):
            return self.fieldsets
        elif self.fields:
            return [(None, {"fields": self.fields})]
        return None

    def get_filterset_class(self) -> type[FilterSet]:
        """
        Returns a dynamically generated FilterSet class for the model.

        Returns:
            Type[FilterSet]: A FilterSet subclass.
        """
        if self.filterset_class is not FilterSet:
            return self._get_class(self.filterset_class)
        return factories.filterset_factory(
            self.model,
            filterset=self._get_class(self.filterset_class),
            **self.filterset_options,
        )

    def get_form_class(self) -> type[ModelForm]:
        """
        Returns a dynamically generated ModelForm class for the model.

        Returns:
            Type[ModelForm]: A ModelForm subclass.
        """
        fields = getattr(self, "form_fields", "__all__")
        return factories.modelform_factory(
            self.model, form=self._get_class(self.form_class), fields=fields, **self.form_options
        )

    def get_serializer_class(self) -> type[ModelSerializer]:
        """
        Returns a dynamically generated ModelSerializer class for the model.

        Returns:
            Type[ModelSerializer]: A ModelSerializer subclass.
        """
        return factories.serializer_factory(
            self.model,
            serializer_class=self._get_class(self.serializer_class),
            **self.serializer_kwargs,
        )

    def get_table_class(self) -> type[Table]:
        """
        Returns a dynamically generated Table class for the model.

        Returns:
            Type[Table]: A django-tables2 Table subclass.
        """
        kwargs = {
            "exclude": [
                "polymorphic_ctype",
                "sample_ptr",
                "measurement_ptr",
                "image",
                "keywords",
                "created",
                "modified",
                "options",
                "tags",
            ],
        }
        # fields = flatten(self.get_fields())
        # if fields:
        #     kwargs["fields"] = fields
        # if self.table_options:
        #     kwargs = {**kwargs, **self.table_options}

        return table_factory(
            self.model,
            table=self._get_class(self.table_class),
            **kwargs,
        )

    def get_resource_class(self) -> type[ModelResource]:
        """
        Returns a dynamically generated ModelResource class for import/export operations.

        Returns:
            Type[ModelResource]: A ModelResource subclass.
        """
        fields = flatten(self.get_fields())
        kwargs = {
            # "fields": fields,
            "exclude": [
                "polymorphic_ctype",
                "sample_ptr",
                "image",
                "keywords",
                "created",
                "modified",
                "options",
                "tags",
            ],
            **self.resource_options,
        }
        return factories.modelresource_factory(
            self.model,
            resource_class=self._get_class(self.resource_class),
            **kwargs,
        )
