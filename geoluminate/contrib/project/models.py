from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db.models import Extent
from django.core.validators import MaxValueValidator as MaxVal
from django.core.validators import MinValueValidator as MinVal
from django.db import models as django_models
from django.forms.models import model_to_dict
from django.templatetags.static import static
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
from multiselectfield.utils import get_max_length
from taggit.managers import TaggableManager

from geoluminate.contrib.gis.models import SiteMixin
from geoluminate.db import models

from . import choices
from .datacite import choices as datacite
from .utils import ProjectQuerySet, PublicObjectsManager


def project_image_path(instance, filename):
    """Returns the path to the image file for the project."""
    return f"projects/{instance.uuid}/cover_img.{filename.split('.')[-1]}"


class Abstract(models.Model):
    image = ProcessedImageField(
        verbose_name=_("image"),
        help_text=_("Upload an image that represents your project."),
        # processors=[ResizeToFit(1200, 630)],
        format="WEBP",
        options={"quality": 60},
        upload_to=project_image_path,
        blank=True,
        null=True,
        default="world_map.webp",
    )

    key_dates = GenericRelation(
        "KeyDate",
        related_query_name="%(app_label)ss",
    )
    descriptions = GenericRelation(
        "Description",
        related_query_name="%(app_label)ss",
    )
    contributors = GenericRelation(
        "Contributor",
        related_query_name="%(app_label)ss",
    )
    # license = License(
    #     help_text=_("Choose an open source license for your project."),
    #     blank=True,
    #     null=True,
    #     on_delete=models.SET_NULL,
    # )

    class Meta:
        abstract = True

    def __str__(self):
        return force_str(self.title)

    def get_absolute_url(self):
        return reverse(f"{type(self).__name__.lower()}_detail", kwargs={"uuid": self.uuid})

    def get_list_url(self):
        return reverse(f"{type(self).__name__.lower()}_list")

    def get_abstract(self):
        """Returns the abstract description of the project."""
        try:
            return self.descriptions.get(type=Description.DESCRIPTION_TYPES.Abstract)
        except Description.DoesNotExist:
            return None

    def get_meta_description(self):
        abstract = self.get_abstract()
        if abstract:
            return abstract.description
        else:
            return None

    def get_meta_image(self):
        if self.image:
            return self.image.url
        return static("img/brand/logo.svg")

    def get_datasets(self):
        return self.datasets.all()

    def get_samples(self):
        return self.samples.all()

    def get_projects(self):
        return self.projects.all()


class Project(Abstract):
    """A project is a collection of datasets and associated metadata. The Project model
    is the top level model in the Geoluminate schema hierarchy and all datasets, samples,
    sites and measurements should relate back to a project."""

    PROJECT_TAGS = choices.ProjectTags
    # objects = PublicObjectsManager()

    STATUS_CHOICES = choices.ProjectStatus

    title = models.CharField(
        _("name"),
        help_text="Give your project a meaningful title that helps others easily understand your aims.",
        max_length=255,
    )

    status = models.IntegerField(_("status"), choices=STATUS_CHOICES.choices, default=STATUS_CHOICES.CONCEPT)

    funding = models.JSONField(
        verbose_name=_("funding"),
        help_text=_("Include details of any funding received for this project."),
        null=True,
        blank=True,
    )

    tags = TaggableManager(help_text=_("Add tags to help others discover your project."), blank=True)

    # flags
    add_dataset_contributors = models.BooleanField(
        _("add dataset contributors"),
        help_text=_(
            "All contributors to datasets associated with this project should be automatically added as a project"
            " member."
        ),
        default=True,
    )
    is_public = models.BooleanField(
        _("visibility"),
        help_text=_("Choose whether this project is publicly discoverable."),
        choices=(
            (True, _("Public")),
            (False, _("Private")),
        ),
        default=False,
    )

    # this should probably be added_by
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        help_text=_(
            "The user who created this project in the context of the application. This is unrelated to the project"
            " itself. I.e. the user who created the entry may have done so on another person's behalf."
        ),
        null=True,
        blank=True,
        related_name="submitted_%(class)ss",
        on_delete=models.SET_NULL,
    )

    _metadata = {
        "title": "title",
        "description": "get_meta_description",
        "image": "get_meta_image",
        "type": "research.project",
    }

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")

    def get_contact_persons(self):
        """Returns all contributors with the ContactPerson role."""
        return self.contributors.filter(roles__contains=choices.ContributorRoles.CONTACT_PERSON)

    def add_contributors(self, *profiles, roles=None):
        """Adds the given profiles as contributors to the object."""
        for profile in profiles:
            self.contributors.create(profile=profile, roles=roles)

    def in_progress(self):
        """Returns True if the project is in progress"""
        return self.status == self.STATUS_CHOICES.IN_PROGRESS

    def get_contributors(self):
        """Returns all contributors of the project"""
        return None

    def lead_contributors(self):
        """Returns all project leads"""
        return self.contributors.filter(roles__contains=choices.ContributorRoles.PROJECT_LEADER)

    def funding_contributors(self):
        """Returns all project leads"""
        return self.contributors.filter(roles__contains=choices.ContributorRoles.SPONSOR)


class Dataset(Abstract):
    """A dataset is a collection of samples, measurements and associated metadata. The Dataset model
    is the second level model in the Geoluminate schema heirarchy and all geographic sites,
    samples and sample measurements MUST relate back to a dataset."""

    reference = models.OneToOneField(
        "literature.Literature",
        help_text=_("The primary reference that this dataset is associated with."),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    project = models.ForeignKey(
        Project,
        verbose_name=_("project"),
        help_text=_("The project that this dataset belongs to."),
        related_name="datasets",
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        verbose_name=_("title"), help_text=_("The name of the dataset."), max_length=255, blank=True
    )

    keywords = TaggableManager(help_text=_("Add keywords to help others discover your dataset."), blank=True)

    # to be set when a reviewer marks this as complete
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        help_text=_("The user who approved this dataset."),
        null=True,
        blank=True,
        related_name="approved_%(class)ss",
        on_delete=models.SET_NULL,
    )

    is_public = models.BooleanField(
        _("visibility"),
        help_text=_("Choose whether this project is publicly discoverable."),
        choices=(
            (True, _("Public")),
            (False, _("Private")),
        ),
        default=False,
    )

    _metadata = {
        "title": "title",
        "description": "get_meta_description",
        "type": "research.dataset",
    }

    class Meta:
        verbose_name = _("dataset")
        verbose_name_plural = _("datasets")

    def get_contact_persons(self):
        """Returns all contributors with the ContactPerson role."""
        return self.contributors.filter(roles__contains=choices.ContributorRoles.CONTACT_PERSON)

    @property
    def resource_type(self):
        """Returns the resource type as per the DataCite schema. Geoluminate datasets are always of type 'Dataset'."""
        return "Dataset"

    def bbox(self):
        """Returns the bounding box of the dataset as a list of coordinates in the format [xmin, ymin, xmax, ymax]."""
        props = model_to_dict(self)
        coords = self.samples.aggregate(Extent("geom"))["geom__extent"]
        return {"type": "Polygon", "coordinates": [coords], "properties": props}


class Location(models.Model):
    name = models.CharField(
        verbose_name=_("name"),
        help_text=_("The name of the location."),
        max_length=255,
        blank=True,
        null=True,
    )
    point = models.PointField(null=True, blank=True)
    polygon = models.PolygonField(null=True, blank=True)

    class Meta:
        verbose_name = _("location")
        verbose_name_plural = _("locations")


class Sample(Abstract):
    """This model attempts to roughly replicate the schema of the International
    Generic Sample Number (IGSN) registry. Each sample in this table MUST belong to
    a `geoluminate.contrib.project.models.Dataset`."""

    # can get more info from www.vocabulary.odsm2
    type = models.CharField(
        verbose_name=_("sample type"),
        null=True,
        help_text=_("The type of sample as per the ODM2 controlled vocabulary."),
        max_length=255,
    )
    title = models.CharField(
        verbose_name=_("name"),
        null=True,
        help_text=_("The name of the sample."),
        max_length=255,
    )
    description = models.TextField(
        _("description"),
        help_text=_("A description of the sample."),
        blank=True,
        null=True,
    )

    location = models.ForeignKey(
        Location,
        verbose_name=_("location"),
        help_text=_("The location of the sample."),
        related_name="samples",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    geom = models.PointField(null=True, blank=True)

    elevation = models.QuantityField(
        base_units="m",
        unit_choices=["m", "ft"],
        verbose_name=_("elevation"),
        help_text=_("Elevation with reference to mean sea level"),
        validators=[MaxVal(9000), MinVal(-12000)],
        blank=True,
        null=True,
    )
    comment = models.TextField(
        _("comment"),
        help_text=_("General comments regarding the site and/or measurement"),
        blank=True,
        null=True,
    )
    acquired = models.DateTimeField(
        _("date acquired"),
        help_text=_("Date and time of acquisition."),
        null=True,
    )

    parent = models.ForeignKey(
        "self", verbose_name=_("parent"), help_text=_("Parent sample"), blank=True, null=True, on_delete=models.CASCADE
    )
    dataset = models.ForeignKey(
        Dataset,
        verbose_name=_("dataset"),
        help_text=_("The dataset to which this sample belongs."),
        related_name="samples",
        on_delete=models.CASCADE,
    )

    _metadata = {
        "title": "title",
        "description": "description",
        "type": "research.dataset",
    }

    class Meta:
        verbose_name = _("sample")
        verbose_name_plural = _("samples")


class Site(Sample, SiteMixin):
    class Meta:
        verbose_name = _("site")
        verbose_name_plural = _("sites")
        proxy = True


class Measurement(models.Model):
    class Meta:
        abstract = True

    def get_absolute_url(self):
        return reverse("site", kwargs={"pk": self.pk})

    def get_quality(self):
        """This method should be implemented by classes that subclass this abstract class. It should return a
        value between 0 and 1 that represents the quality of the measurement."""
        raise NotImplementedError


class Contributor(django_models.Model):
    """A contributor is a person or organisation that has contributed to the project or
    dataset. This model is based on the Datacite schema for contributors."""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    CONTRIBUTOR_ROLES = choices.ContributorRoles
    PERSONAL_ROLES = choices.PersonalRoles
    ORGANIZATIONAL_ROLES = choices.OrganizationalRoles
    OTHER_ROLES = choices.OtherRoles

    roles = models.MultiSelectField(
        choices=CONTRIBUTOR_ROLES.choices,
        max_length=get_max_length(CONTRIBUTOR_ROLES.choices, None),
        verbose_name=_("roles"),
        help_text=_("Contributor roles as per the Datacite ContributorType vocabulary."),
    )
    profile = models.ForeignKey(
        "user.Profile",
        verbose_name=_("contributor"),
        help_text=_("The person or organisation that contributed to the project or dataset."),
        related_name="contributions",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("contributor")
        verbose_name_plural = _("contributors")
        unique_together = ("profile", "content_type", "object_id")
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        return force_str(self.profile)

    # def __repr__(self):
    #     return f"<{self.__class__.__name__}: {self}>"

    def get_absolute_url(self):
        """Returns the absolute url of the contributor's profile."""
        return self.profile.get_absolute_url()

    def roles_list(self):
        """Returns a string containg a '|' separated list of the contributor's roles."""
        return "|".join(self.roles)


class KeyDate(django_models.Model):
    class DateTypes(models.TextChoices):
        PROPOSED_START = "proposed_start", _("Proposed start")
        PROPOSED_END = "proposed_end", _("Proposed end")
        START = "start", _("Start")
        END = "end", _("End")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    type = models.CharField(
        _("type"),
        help_text=_("The type of date."),
        max_length=255,
        choices=DateTypes.choices,
        default=DateTypes.PROPOSED_START,
    )
    date = models.DateTimeField(_("date"), help_text=_("The date."))

    class Meta:
        verbose_name = _("key date")
        verbose_name_plural = _("key dates")
        ordering = ["date"]
        unique_together = ("type", "content_type", "object_id")
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class Description(django_models.Model):
    DESCRIPTION_TYPES = datacite.get_choices_for("descriptionType")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    type = models.CharField(
        _("type"),
        max_length=32,
        choices=DESCRIPTION_TYPES.choices,
        default=DESCRIPTION_TYPES.Abstract,
    )
    description = models.TextField(_("description"))
    # content = models.TextField(_("content"))

    class Meta:
        verbose_name = _("description")
        verbose_name_plural = _("descriptions")
        # unique_together = ("type", "content_type", "object_id")
        # indexes = [
        #     models.Index(fields=["content_type", "object_id"]),
        # ]


def get_measurement_types():
    """Get a list of all models in the project that subclass from :class:`geoluminate.db.models.Base`."""
    measurment_types = []

    for model in apps.get_models():
        if issubclass(model, Measurement):
            measurment_types.append(model)
    return measurment_types
