from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db.models import Collect, Extent
from django.contrib.gis.measure import Distance
from django.core.validators import MaxValueValidator as MaxVal
from django.core.validators import MinValueValidator as MinVal
from django.db import models as django_models
from django.forms.models import model_to_dict
from django.templatetags.static import static
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from multiselectfield.utils import get_max_length
from taggit.managers import TaggableManager

from geoluminate import models

# from geoluminate.utils.gis.managers import LocationManager
from . import choices

# from .datacite import choices as datacite


def project_image_path(instance, filename):
    """Returns the path to the image file for the project."""
    return f"projects/{instance.uuid}/cover_img.{filename.split('.')[-1]}"


class Abstract(models.Model):
    """An abstract model that contains common fields and methods for both the Project and Dataset models."""

    DISCOVERY_TAGS = choices.DiscoveryTags

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
    title = models.CharField(
        _("name"),
        help_text="The title of the object.",
        max_length=255,
    )
    keywords = TaggableManager(
        verbose_name=_("keywords"), help_text=_("Add keywords to help others discover your work."), blank=True
    )
    tags = models.MultiSelectField(
        choices=DISCOVERY_TAGS,
        max_length=32,
        verbose_name=_("tags"),
        help_text=_("Tags to help others discover your project."),
        blank=True,
        null=True,
    )
    key_dates = GenericRelation(
        "KeyDate",
        verbose_name=_("key dates"),
        related_name="%(app_label)ss",
        related_query_name="%(app_label)ss",
        help_text=_("Add some key dates."),
    )
    descriptions = GenericRelation(
        "Description",
        verbose_name=_("descriptions"),
        related_name="%(app_label)ss",
        related_query_name="%(app_label)ss",
        help_text=_("Add some descriptions."),
    )
    contributors = GenericRelation(
        "Contribution",
        verbose_name=_("contributors"),
        related_name="%(app_label)ss",
        related_query_name="%(app_label)ss",
        help_text=_("Add some contributors."),
    )

    funding = models.JSONField(
        verbose_name=_("funding"),
        help_text=_("Include details of any funding received for this project."),
        null=True,
        blank=True,
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

    def get_contact_persons(self):
        """Returns all contributors with the ContactPerson role."""
        return self.contributors.filter(roles__contains=choices.ContributionnnRoles.CONTACT_PERSON)


class Project(Abstract):
    """A project is a collection of datasets and associated metadata. The Project model
    is the top level model in the Geoluminate schema hierarchy and all datasets, samples,
    and measurements should relate back to a project."""

    STATUS_CHOICES = choices.ProjectStatus

    # objects = PublicObjectsManager()

    status = models.IntegerField(_("status"), choices=STATUS_CHOICES.choices, default=STATUS_CHOICES.CONCEPT)

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

    _metadata = {
        "title": "title",
        "description": "get_meta_description",
        "image": "get_meta_image",
        "type": "research.project",
    }

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")

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
        return self.contributors.filter(roles__contains=choices.ContributionRoles.PROJECT_LEADER)

    def funding_contributors(self):
        """Returns all project leads"""
        return self.contributors.filter(roles__contains=choices.ContributionRoles.SPONSOR)


class Dataset(Abstract):
    """A dataset is a collection of samples, measurements and associated metadata. The Dataset model
    is the second level model in the Geoluminate schema heirarchy and all geographic sites,
    samples and sample measurements MUST relate back to a dataset."""

    reference = models.OneToOneField(
        "literature.Literature",
        help_text=_(
            "The data publication to which this dataset belongs. If the dataset has not been formally published, leave"
            " this field blank."
        ),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    related_literature = models.ManyToManyField(
        "literature.Literature",
        help_text=_("Any literature that is related to this dataset."),
        related_name="related_datasets",
        related_query_name="related_dataset",
        blank=True,
    )
    project = models.ForeignKey(
        Project,
        verbose_name=_("project"),
        help_text=_("The project that this dataset belongs to."),
        related_name="datasets",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

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

    @property
    def resource_type(self):
        """Returns the resource type as per the DataCite schema. Geoluminate datasets are always of type 'Dataset'."""
        return "Dataset"

    def bbox(self):
        """Returns the bounding box of the dataset as a list of coordinates in the format [xmin, ymin, xmax, ymax]."""
        props = model_to_dict(self)
        coords = (
            self.samples.prefetch_related("location")
            .values("location__point")
            .aggregate(Extent("location__point"))["location__point__extent"]
        )
        return {"type": "Polygon", "coordinates": [coords], "properties": props}

    def as_collection(self):
        """Returns a GeometryCollection of all the samples in the dataset"""
        qs = self.samples.select_related("location").values("location__point")
        return qs.aggregate(Collect("location__point"))["location__point__collection"]


class Location(models.Model):
    # objects = LocationManager.as_manager()

    name = models.CharField(
        verbose_name=_("name"),
        help_text=_("The name of the location."),
        max_length=255,
        blank=True,
        null=True,
    )
    point = models.PointField(null=True, blank=True)
    polygon = models.PolygonField(null=True, blank=True)
    elevation = models.QuantityField(
        base_units="m",
        unit_choices=["m", "ft"],
        verbose_name=_("elevation"),
        help_text=_("Elevation with reference to mean sea level"),
        validators=[MaxVal(9000), MinVal(-12000)],
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("location")
        verbose_name_plural = _("locations")

    @property
    def latitude(self):
        """Convenience method for retrieving the site's latitude ordinate."""
        return self.point.y

    @latitude.setter
    def latitude(self, val):
        self.point.y = val

    @property
    def longitude(self):
        """Convenience method for retrieving the site's longitude ordinate."""
        return self.point.x

    @longitude.setter
    def longitude(self, val):
        self.point.x = val

    @property
    def lon(self):
        """Alias of self.longitude"""
        return self.longitude

    @lon.setter
    def lon(self, val):
        self.point.x = val

    @property
    def lat(self):
        """Alias of self.latitude"""
        return self.latitude

    @lat.setter
    def lat(self, val):
        self.point.y = val

    def __str__(self):
        """Returns the string representation of this site"""
        return f"{self.lat}, {self.lon}"

    def get_absolute_url(self):
        """Returns the absolute URL for this site"""
        raise NotImplementedError

    def get_sites_within(self, radius=25):
        """Gets nearby sites within {radius} km radius"""
        return self.objects.filter(point__distance_lt=(self.point, Distance(km=radius)))


class Sample(Abstract):
    """This model attempts to roughly replicate the schema of the International
    Generic Sample Number (IGSN) registry. Each sample in this table MUST belong to
    a `geoluminate.contrib.core.models.Dataset`."""

    # can get more info from www.vocabulary.odsm2
    type = models.CharField(
        choices=[(x, x) for x in settings.GEOLUMINATE_SAMPLE_TYPES],
        verbose_name=_("sample type"),
        default=settings.GEOLUMINATE_DEFAULT_SAMPLE_TYPE,
        help_text=_("The type of sample as per the ODM2 controlled vocabulary."),
        max_length=255,
    )
    name = models.CharField(
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


class Measurement(models.Model):
    sample = models.ForeignKey(
        Sample,
        verbose_name=_("sample"),
        help_text=_("The sample on which the measurement was made."),
        on_delete=models.PROTECT,
    )

    class Meta:
        abstract = True

    @cached_property
    def get_sample(self):
        return self.sample

    @cached_property
    def get_location(self):
        return self.sample.location

    def get_absolute_url(self):
        return reverse("site", kwargs={"pk": self.pk})


class Contribution(django_models.Model):
    """A contributor is a person or organisation that has contributed to the project or
    dataset. This model is based on the Datacite schema for contributors."""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    CONTRIBUTOR_ROLES = choices.ContributionRoles
    PERSONAL_ROLES = choices.PersonalRoles
    ORGANIZATIONAL_ROLES = choices.OrganizationalRoles
    OTHER_ROLES = choices.OtherRoles

    roles = models.MultiSelectField(
        choices=CONTRIBUTOR_ROLES.choices,
        max_length=get_max_length(CONTRIBUTOR_ROLES.choices, None),
        verbose_name=_("roles"),
        help_text=_("Contribution roles as per the Datacite ContributionType vocabulary."),
    )
    profile = models.ForeignKey(
        "user.Contributor",
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
    # DESCRIPTION_TYPES = datacite.get_choices_for("descriptionType")
    DESCRIPTION_TYPES = choices.DataCiteDescriptionTypes
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    type = models.CharField(
        _("type"),
        max_length=32,
        choices=DESCRIPTION_TYPES.choices,
        default=DESCRIPTION_TYPES.ABSTRACT,
    )
    text = models.TextField(_("description"))
    # content = models.TextField(_("content"))

    class Meta:
        verbose_name = _("description")
        verbose_name_plural = _("descriptions")
        # unique_together = ("type", "content_type", "object_id")
        # indexes = [
        #     models.Index(fields=["content_type", "object_id"]),
        # ]


class Review(models.Model):
    """Stores information about each review"""

    dataset = models.OneToOneField(
        to="Dataset",
        help_text=_("Dataset being reviewed"),
        on_delete=models.SET_NULL,
        null=True,
    )
    reviewer = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        help_text=_("User reviewing this publication"),
        on_delete=models.SET_NULL,
        null=True,
    )
    submitted = models.DateTimeField(
        verbose_name=_("date submitted"),
        help_text=_("Date the user submitted correction for final approval by site admins"),
        null=True,
        blank=True,
    )
    accepted = models.DateTimeField(
        verbose_name=_("date accepted"),
        help_text=_("Date the review was accepted by site admins and incorporated into the production database"),
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Review of {self.dataset} by {self.reviewer}"


def get_measurement_types():
    """Get a list of all models in the project that subclass from :class:`geoluminate.models.Base`."""
    measurment_types = []

    for model in apps.get_models():
        if issubclass(model, Measurement):
            measurment_types.append(model)
    return measurment_types
