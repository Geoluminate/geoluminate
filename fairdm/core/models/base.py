from typing import Any

from django.apps import apps
from django.db import models
from django.forms import ModelForm
from django.utils.decorators import classonlymethod
from django.utils.module_loading import import_string
from django_filters import FilterSet
from django_tables2 import Table, table_factory
from import_export.resources import ModelResource
from polymorphic.base import PolymorphicModelBase
from research_vocabs.core import Concept
from rest_framework.serializers import ModelSerializer

from fairdm.metadata import Authority, Citation
from fairdm.utils import factories
from fairdm.utils.utils import get_inheritance_chain, get_subclasses


class AppLevelConfig:
    def __init__(self, app_config):
        self.authority = getattr(app_config, "authority", None)
        self.maintainer = getattr(app_config, "maintainer", None)
        self.repository_url = getattr(app_config, "repository_url", None)
        self.keywords = getattr(app_config, "keywords", [])
        self.citation = getattr(app_config, "citation", [])


class Config:
    """
    A configuration class that dynamically generates and manages various framework-specific
    components (filterset, serializer, form, table, resource) for a given Django model.

    The following FairDM innerclass attributes are supported:

    - filterset_class (str | Type[FilterSet]): The FilterSet class or path to the FilterSet class.
    - filterset_kwargs (dict): Additional keyword arguments to pass to the FilterSet class.
    - serializer_class (str | Type[ModelSerializer]): The ModelSerializer class or path to the ModelSerializer class.
    - serializer_kwargs (dict): Additional keyword arguments to pass to the ModelSerializer class.
    - form_class (str | Type[ModelForm]): The ModelForm class or path to the ModelForm class.
    - form_fields (list[str]): The fields to include in the ModelForm.
    - form_kwargs (dict): Additional keyword arguments to pass to the ModelForm class.
    - table_class (str | Type[Table]): The Table class or path to the Table class.
    - table_kwargs (dict): Additional keyword arguments to pass to the Table class.
    - resource_class (str | Type[ModelResource]): The ModelResource class or path to the ModelResource class.
    - resource_kwargs (dict): Additional keyword arguments to pass to the ModelResource class.
    """

    CONFIG_OPTIONS = [
        "filterset_class",
        "filterset_kwargs",
        "serializer_class",
        "serializer_kwargs",
        "form_class",
        "form_fields",
        "form_kwargs",
        "table_class",
        "table_kwargs",
        "resource_class",
        "resource_kwargs",
        "fields",
    ]
    filterset_class: type[FilterSet] = FilterSet
    """The FilterSet class or path to the FilterSet class."""

    filterset_kwargs: dict = {}
    """Additional keyword arguments to pass to the FilterSet class."""

    serializer_class: type[ModelSerializer] = ModelSerializer
    """The ModelSerializer class or path to the ModelSerializer class."""

    serializer_kwargs: dict = {}
    """Additional keyword arguments to pass to the ModelSerializer class."""

    form_class: type[ModelForm] = ModelForm
    """The ModelForm class or path to the ModelForm class."""

    form_kwargs: dict = {}
    """Additional keyword arguments to pass to the ModelForm class."""

    table_class: type[Table] = Table
    """The Table class or path to the Table class."""

    table_kwargs: dict = {}
    """Additional keyword arguments to pass to the Table class."""

    resource_class: type[ModelResource] = ModelResource
    """The ModelResource class or path to the ModelResource class."""

    resource_kwargs: dict = {}
    """Additional keyword arguments to pass to the ModelResource class."""

    export_fields = []

    fields: list[str] = []

    fieldsets: list[Any] = []

    def __init__(self, model_class: type[Any], fairdm: Any, inherited: dict, app_config: Any):
        """
        Initializes the Config instance.

        Args:
            model_class (Type[Any]): The Django model class.
            fairdm (Any): The FairDM inner class instance containing metadata.
            inherited (Any): FairDM config data from an inherited model class.
            app_config (Any): The app configuration instance.
        """

        # merge fairdm, app_config and inherited_config with priority in that order
        # Priority order: fairdm > app_config > inherited_config
        if inherited is not None:
            merged = {**inherited.config.__dict__, **app_config.__dict__, **fairdm.__dict__}
        else:
            merged = {**app_config.__dict__, **fairdm.__dict__}

        # Set attributes from merged_attrs
        for attr, value in merged.items():
            if attr in self.CONFIG_OPTIONS:
                setattr(self, attr, value)

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
            return None

        if "id" not in self.fields:
            return ["id", "dataset"] + self.fields
        return self.fields

    def get_filterset_class(self) -> type[FilterSet]:
        """
        Returns a dynamically generated FilterSet class for the model.

        Returns:
            Type[FilterSet]: A FilterSet subclass.
        """
        return factories.filterset_factory(
            self.model,
            filterset=self._get_class(self.filterset_class),
            **self.filterset_kwargs,
        )

    def get_form_class(self) -> type[ModelForm]:
        """
        Returns a dynamically generated ModelForm class for the model.

        Returns:
            Type[ModelForm]: A ModelForm subclass.
        """
        fields = getattr(self, "form_fields", "__all__")
        return factories.modelform_factory(
            self.model, form=self._get_class(self.form_class), fields=fields, **self.form_kwargs
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
        return table_factory(
            self.model,
            table=self._get_class(self.table_class),
            **self.table_kwargs,
        )

    def get_resource_class(self) -> type[ModelResource]:
        """
        Returns a dynamically generated ModelResource class for import/export operations.

        Returns:
            Type[ModelResource]: A ModelResource subclass.
        """
        kwargs = {
            "fields": self.get_fields(),
            "exclude": [
                "polymorphic_ctype",
                "sample_ptr",
                "image",
                "keywords",
                "created",
                "modified",
                "options",
                "test",
                "tags",
            ],
            **self.resource_kwargs,
        }
        return factories.modelresource_factory(
            self.model,
            resource_class=self._get_class(self.resource_class),
            **kwargs,
        )


class Metadata:
    """
    Represents metadata for a data model.

    Attributes:
        name (str): The name of the model.
        name_plural (str): The pluralized name of the model.
        description (str): A detailed description of the data model. This is required.
        authority (Authority | None): The authority that created this metadata. This is required.
        maintainer (str): The package maintainer of the data model.
        repository_url (str): The URL of the repository where the data model can be viewed.
        keywords (list[Concept]): A list of controlled keywords that describe the data model.
        citation (list[Citation]): The citation(s) for the data model.
    """

    def __init__(self, model_class, new_meta, old_meta, app_config):
        self.name: str = getattr(new_meta, "name", None) or getattr(model_class._meta, "verbose_name", None)
        self.name_plural: str = getattr(new_meta, "name_plural", None) or getattr(
            model_class._meta, "verbose_name_plural", None
        )

        if not hasattr(new_meta, "description"):
            raise ValueError("Metadata description is required")
        self.description: str = new_meta.description

        self.authority: Authority | None = getattr(new_meta, "authority", None) or getattr(
            app_config, "authority", None
        )
        if self.authority is not None and not isinstance(self.authority, Authority):
            raise ValueError("Metadata item `authority` must be an Authority instance.")

        self.maintainer: str = getattr(new_meta, "maintainer", None) or getattr(app_config, "maintainer", None)

        self.repository_url: str = getattr(new_meta, "repository_url", None) or getattr(
            app_config, "repository_url", None
        )
        if not self.repository_url:
            raise ValueError(
                "Metadata item `repository_url` is required and must be defined in the model FairDM class or the applications AppConfig."
            )

        self.keywords: list[Concept] = getattr(new_meta, "keywords", []) + getattr(app_config, "keywords", [])
        if getattr(old_meta, "keywords", None):
            self.keywords += old_meta.keywords

        new_meta_citations = getattr(new_meta, "citation", [])
        if isinstance(new_meta_citations, Citation):
            new_meta_citations = [new_meta_citations]

        app_config_citations = getattr(app_config, "citation", [])
        if isinstance(app_config_citations, Citation):
            app_config_citations = [app_config_citations]

        self.citation: list[Citation] = new_meta_citations + app_config_citations
        if not all(isinstance(c, Citation) for c in self.citation):
            raise ValueError("Metadata item `citation` must be a Citation instance.")

    def to_dict(self) -> dict:
        """
        Returns a serializable dictionary of the metadata attributes.

        Returns:
            dict: A dictionary representation of the metadata.
        """
        # Manually handle citation to ensure it's a list of dictionaries
        citations = [citation.as_dict() if isinstance(citation, Citation) else citation for citation in self.citation]

        return {
            "name": self.name,
            "name_plural": self.name_plural,
            "description": self.description,
            "authority": self.authority.as_dict() if self.authority else None,
            "keywords": [keyword.as_dict() if isinstance(keyword, Concept) else keyword for keyword in self.keywords],
            "repository_url": self.repository_url,
            "maintainer": self.maintainer,
            "citation": citations,
        }


class FairDMOptions:
    """
    Handles the configuration and metadata for the FairDM model, including
    managing the model hierarchy and citations.

    Attributes:
        heirarchy (list): List of base FairDM options, representing model inheritance.
        config (Config): Configuration for the model, including form, filter, serializer, etc.
        meta (Metadata): Metadata associated with the model, including description, authority, etc.
    """

    def __init__(self, model_class, fairdm, inherited_config, app_config):
        """
        Initialize the FairDMOptions with the model, configuration, and metadata.

        Args:
            model_class (Model): The model class being processed.
            fairdm (FairDM): The FairDM instance with the model's specific settings.
            inherited_config (FairDM or None): The base FairDM from which the model inherits.
            app_config (AppConfig): The app configuration that may contain additional settings.

        Notes:
            - Initializes `heirarchy` from the base FairDM if present.
            - Merges `Config` and `Metadata` based on the provided classes.
        """
        self.heirarchy = getattr(inherited_config, "heirarchy", [])
        self.config = Config(model_class, fairdm, inherited_config, app_config)
        self.meta = Metadata(model_class, fairdm, inherited_config, app_config)

    def get_citations(self):
        """
        Collects and returns all citation information from the current model's metadata
        and any parent models in the hierarchy.

        Returns:
            list: A list of Citation instances from the current model and its parent models.

        Notes:
            - Citations are gathered from `meta.citation` and merged from the `heirarchy` models.
            - Each item in the list is validated as a `Citation` instance.
        """
        citations = self.meta.citation
        # Collect citations from each parent in the heirarchy
        for item in self.heirarchy:
            citations += item.meta.citation
        return citations


class FairDMBase(PolymorphicModelBase):
    """
    Metaclass that merges FairDM inner classes of parent classes into the current class.

    This metaclass ensures that any parent class inheriting from FairDM will have its
    FairDM configuration merged into the current class. It also ensures compatibility
    with django-polymorphic by subclassing `PolymorphicModelBase`.

    FairDM metadata and configuration options are available on the class as `_fairdm`.
    """

    def __new__(cls, name, bases, attrs):
        """
        Custom class creation method that merges the FairDM configuration from parent classes.

        - Searches for any parent classes inheriting from FairDM.
        - Merges the FairDM configurations of the parent class into the new class.
        - Adds a `FairDMOptions` instance to the class to handle options and metadata.

        FairDM metadata and configuration options are accessible on the class as `_fairdm`.

        Args:
            cls (type): The metaclass.
            name (str): The name of the class being created.
            bases (tuple): The base classes of the class.
            attrs (dict): The attributes of the class being created.

        Returns:
            type: The new class with merged configurations and metadata.
        """
        # Find parent classes that are instances of FairDMBase
        parents = [b for b in bases if isinstance(b, FairDMBase)]

        if not parents:
            # If no parent class inherits from FairDMBase, proceed with default behavior
            return super().__new__(cls, name, bases, attrs)

        # Extract the FairDM attribute from the class attributes
        fairdm = attrs.pop("FairDM", None)
        module = attrs.get("__module__", None)
        app_config = apps.get_containing_app_config(module)

        # Create the new class
        new_class = super().__new__(cls, name, bases, attrs)

        # If no FairDM configuration found, fallback to the class-level FairDM attribute
        # fairdm = fairdm or getattr(new_class, "FairDM", None)

        # Retrieve the base class's FairDM configuration (if any)
        inherited_config = getattr(new_class, "_fairdm", None)

        # If FairDM is provided, merge configurations into the new class
        if fairdm:
            options = FairDMOptions(new_class, fairdm, inherited_config, AppLevelConfig(app_config))
            new_class.add_to_class("_fairdm", options)

        return new_class


class FairDMModel(models.Model):
    class Meta:
        abstract = True

    @classonlymethod
    def get_subclasses(cls):
        return get_subclasses(cls)

    @classonlymethod
    def get_inheritance_chain(cls):
        return get_inheritance_chain(cls, cls.base_class())
