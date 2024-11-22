from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse

# from rest_framework.authtoken.models import Token
from django.utils.functional import cached_property
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from licensing.fields import LicenseField
from meta.models import ModelMeta
from model_utils import FieldTracker
from polymorphic.models import PolymorphicModel
from polymorphic_treebeard.models import PolymorphicMP_Node
from research_vocabs.fields import ConceptField
from shortuuid.django_fields import ShortUUIDField

from geoluminate.core.choices import Visibility
from geoluminate.core.models import PolymorphicMixin
from geoluminate.core.utils import default_image_path
from geoluminate.metadata import Metadata

from .choices import ProjectStatus, SampleStatus
from .vocabularies import FairDMDates, FairDMDescriptions, FairDMRoles


class BaseModel(ModelMeta, models.Model):
    image = ThumbnailerImageField(
        verbose_name=_("image"),
        blank=True,
        null=True,
        upload_to=default_image_path,
    )
    name = models.CharField(_("name"), max_length=255)

    keywords = models.ManyToManyField(
        "research_vocabs.Concept",
        verbose_name=_("keywords"),
        help_text=_("Controlled keywords for enhanced discoverability"),
        blank=True,
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created",
        help_text="When this record was created.",
    )
    modified = models.DateTimeField(
        auto_now=True,
        verbose_name="Modified",
        help_text="When this record was last modified.",
    )

    options = models.JSONField(
        verbose_name=_("options"),
        null=True,
        blank=True,
    )

    tracker = FieldTracker()

    _metadata: Metadata = None

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name}"

    @property
    def title(self):
        return self.name

    # def __init_subclass__(cls, **kwargs):
    #     super().__init_subclass__(**kwargs)
    #     cls.descriptions = GenericRelation("generic.Description", related_query_name=cls.__name__.lower())
    #     cls.dates = GenericRelation("generic.Date", related_query_name=cls.__name__.lower())
    #     cls.identifiers = GenericRelation("generic.Identifier", related_query_name=cls.__name__.lower())
    #     cls.contributors = GenericRelation("contributors.Contribution", related_query_name=cls.__name__.lower())

    def get_absolute_url(self):
        return reverse(f"{self._meta.model_name}-detail", kwargs={"pk": self.pk})

    def get_api_url(self):
        return reverse(f"api:{self._meta.model_name}-detail", kwargs={"pk": self.pk})

    def is_contributor(self, user):
        """Returns true if the user is a contributor."""

        return self.contributions.filter(contributor=user).exists()

    def get_abstract(self):
        """Returns the abstract description of the project."""
        try:
            return self.descriptions.get(type="Abstract")
        except self.DoesNotExist:
            return None

    def get_meta_description(self):
        abstract = self.get_abstract()
        if abstract:
            return abstract.description
        else:
            return None

    @cached_property
    def get_descriptions(self):
        descriptions = list(self.descriptions.all())
        # descriptions.sort(key=lambda x: self.DESCRIPTION_TYPES.values.index(x.type))
        return descriptions


class Project(BaseModel):
    """A project is a collection of datasets and associated metadata. The Project model
    is the top level model in the Geoluminate schema hierarchy and all datasets, samples,
    and measurements should relate back to a project."""

    CONTRIBUTOR_ROLES = FairDMRoles.from_collection("Project")
    DATE_TYPES = FairDMDates.from_collection("Project")
    DESCRIPTION_TYPES = FairDMDescriptions.from_collection("Project")
    # IDENTIFIER_TYPES = choices.DataCiteIdentifiers
    STATUS_CHOICES = ProjectStatus
    VISIBILITY = Visibility

    id = ShortUUIDField(
        editable=False,
        unique=True,
        prefix="p",
        verbose_name="UUID",
        primary_key=True,
    )

    visibility = models.IntegerField(
        _("visibility"),
        choices=VISIBILITY,
        default=VISIBILITY.PRIVATE,
        help_text=_("Visibility within the application."),
    )
    funding = models.JSONField(
        verbose_name=_("funding"),
        help_text=_("Related funding information."),
        null=True,
        blank=True,
    )
    status = models.IntegerField(_("status"), choices=STATUS_CHOICES, default=STATUS_CHOICES.CONCEPT)
    # snippet = models.CharField(_("snippet"), blank=True, null=True, max_length=512)
    # GENERIC RELATIONS
    descriptions = GenericRelation("generic.Description")
    dates = GenericRelation("generic.Date")
    identifiers = GenericRelation("generic.Identifier")
    contributors = GenericRelation("contributors.Contribution")

    # RELATIONS
    owner = models.ForeignKey(
        "contributors.Organization",
        on_delete=models.PROTECT,
        related_name="owned_projects",
        verbose_name=_("owner"),
        null=True,
        blank=True,
    )

    _metadata = {
        "title": "name",
        "description": "get_meta_description",
        "image": "get_meta_image",
        "type": "research.project",
    }

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")
        default_related_name = "projects"
        ordering = ["-modified"]


class Dataset(BaseModel):
    """A dataset is a collection of samples, measurements and associated metadata. The Dataset model
    is the second level model in the Geoluminate schema heirarchy and all geographic sites,
    samples and sample measurements MUST relate back to a dataset."""

    CONTRIBUTOR_ROLES = FairDMRoles.from_collection("Dataset")
    DATE_TYPES = FairDMDates.from_collection("Dataset")
    DESCRIPTION_TYPES = FairDMDescriptions.from_collection("Dataset")
    # IDENTIFIER_TYPES = choices.DataCiteIdentifiers
    VISIBILITY_CHOICES = Visibility

    id = ShortUUIDField(
        editable=False,
        unique=True,
        prefix="d",
        verbose_name="UUID",
        primary_key=True,
    )

    visibility = models.IntegerField(
        _("visibility"),
        choices=VISIBILITY_CHOICES,
        default=VISIBILITY_CHOICES.PRIVATE,
        help_text=_("Visibility within the application."),
    )

    # GENERIC RELATIONS
    descriptions = GenericRelation("generic.Description")
    dates = GenericRelation("generic.Date")
    identifiers = GenericRelation("generic.Identifier")
    contributors = GenericRelation("contributors.Contribution", related_query_name="dataset")

    # RELATIONS
    project = models.ForeignKey(
        "fairdm.Project",
        verbose_name=_("project"),
        help_text=_("The project associated with the dataset."),
        related_name="datasets",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    reference = models.OneToOneField(
        "literature.LiteratureItem",
        help_text=_("The data publication associated with this dataset."),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    related_literature = models.ManyToManyField(
        "literature.LiteratureItem",
        help_text=_("Any literature that is related to this dataset."),
        related_name="related_datasets",
        related_query_name="related_dataset",
        blank=True,
    )
    license = LicenseField(null=True, blank=True)

    _metadata = {
        "title": "name",
        "description": "get_meta_description",
        "type": "research.dataset",
    }

    class Meta:
        verbose_name = _("dataset")
        verbose_name_plural = _("datasets")
        default_related_name = "datasets"

    @property
    def measurements(self):
        return Measurement.objects.filter(sample__dataset=self)


class Sample(BaseModel, PolymorphicMixin, PolymorphicMP_Node):
    """A sample is a physical or digital object that is part of a dataset."""

    CONTRIBUTOR_ROLES = FairDMRoles.from_collection("Sample")
    DATE_TYPES = FairDMDates.from_collection("Sample")
    DESCRIPTION_TYPES = FairDMDescriptions.from_collection("Sample")
    # IDENTIFIER_TYPES = choices.DataCiteIdentifiers

    id = ShortUUIDField(
        editable=False,
        unique=True,
        prefix="s",
        verbose_name="UUID",
        primary_key=True,
    )
    internal_id = models.CharField(
        _("internal ID"),
        max_length=255,
        help_text=_("An alphanumeric identifier used by the creator/s to identify the sample within a dataset"),
    )

    status = ConceptField(
        verbose_name=_("status"),
        vocabulary=SampleStatus,
        default="unknown",
    )

    # GENERIC RELATIONS
    descriptions = GenericRelation("generic.Description")
    dates = GenericRelation("generic.Date")
    identifiers = GenericRelation("generic.Identifier")
    contributors = GenericRelation("contributors.Contribution")

    # RELATIONS
    dataset = models.ForeignKey(
        "fairdm.Dataset",
        verbose_name=_("dataset"),
        help_text=_("The original dataset this sample first appeared in."),
        related_name="samples",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("sample")
        verbose_name_plural = _("samples")
        ordering = ["created"]
        default_related_name = "samples"

    class Config:
        # metadata = None
        filterset_class = "geoluminate.contrib.core.filters.SampleFilter"
        table_class = "geoluminate.contrib.core.tables.SampleTable"

    @staticmethod
    def base_class():
        # this is required for many of the class methods in PolymorphicMixin
        return Sample

    def get_absolute_url(self):
        return reverse("sample-detail", kwargs={"pk": self.pk})


class Measurement(BaseModel, PolymorphicMixin, PolymorphicModel):
    CONTRIBUTOR_ROLES = FairDMRoles.from_collection("Measurement")
    DESCRIPTION_TYPES = FairDMDescriptions.from_collection("Measurement")
    DATE_TYPES = FairDMDates.from_collection("Measurement")

    id = ShortUUIDField(
        editable=False,
        unique=True,
        prefix="m",
        verbose_name="UUID",
        primary_key=True,
    )

    # GENERIC RELATIONS
    descriptions = GenericRelation("generic.Description")
    dates = GenericRelation("generic.Date")
    identifiers = GenericRelation("generic.Identifier")
    contributors = GenericRelation("contributors.Contribution")

    # RELATIONS
    sample = models.ForeignKey(
        "fairdm.Sample",
        verbose_name=_("sample"),
        help_text=_("The sample on which the measurement was made."),
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = _("measurement")
        verbose_name_plural = _("measurements")
        ordering = ["-modified"]
        default_related_name = "measurements"

    @staticmethod
    def base_class():
        # this is required for many of the class methods in PolymorphicMixin
        return Measurement

    def get_absolute_url(self):
        return self.sample.get_absolute_url()
