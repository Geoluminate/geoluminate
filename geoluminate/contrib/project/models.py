from django.conf import settings
from django.core.validators import MaxValueValidator as MaxVal
from django.core.validators import MinValueValidator as MinVal
from django.db.models import Model
from django.db.models.query import QuerySet
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from geoluminate.db import models


class DateTimeChoices(models.TextChoices):
    """A class for storing choices for DateTimeField models. To use with fuzzy dates."""

    YEAR = "%Y", _("Year")
    MONTH = "%M", _("Month")
    DAY = "%d", _("Day")
    HOUR = "%h", _("Hour")
    MINUTE = "%m", _("Minute")
    SECOND = "%s", _("Second")


class ProjectQuerySet(QuerySet):
    """Custom queryset for the Project model that adds useful methods for filtering
    projects by status."""

    def active(self):
        """Return active projects"""
        return self.filter(status=Project.ACTIVE)

    def inactive(self):
        """Return inactive projects"""
        return self.filter(status=Project.INACTIVE)


class Project(models.Model):
    """A project is a collection of datasets and associated metadata. The Project model
    is the top level model in the Geoluminate schema heirarchy and all datasets, samples,
    sites and measurements should relate back to a project."""

    objects = ProjectQuerySet.as_manager()

    class ProjectStatus(models.IntegerChoices):
        CONCEPT = 0, _("Concept")
        PLANNING = 1, _("Planning")
        # SEARCHING_FOR_FUNDING = 3, _("Searching for funding")
        # SEARCHING_FOR_COLLABORATORS = 4, _("Searching for collaborators")
        IN_PROGRESS = 2, _("In progress")
        COMPLETE = 3, _("Complete")

    name = models.CharField(_("name"), help_text=_("The project title."), max_length=255)
    description = models.TextField(
        _("description"),
        help_text=_("A description of the project and expected outcomes."),
        blank=True,
        null=True,
    )
    lead = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("project lead"),
        help_text=_("This person will be acknowledged as the project leader."),
        related_name="%(class)s_as_lead",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    status = models.IntegerField(_("status"), choices=ProjectStatus.choices, default=ProjectStatus.CONCEPT)

    projected_start_date = models.DateTimeField(
        _("projected start date"),
        help_text=_("Projected start date of the project."),
        blank=True,
        null=True,
    )
    projected_end_date = models.DateTimeField(
        _("projected end date"),
        help_text=_("Projected end date of the project."),
        blank=True,
        null=True,
    )

    start_date = models.DateTimeField(
        _("start date"),
        help_text=_("Start date of the survey."),
        blank=True,
        null=True,
    )
    end_date = models.DateTimeField(_("end date"), help_text=_("End date of the survey."), blank=True, null=True)

    # license = License(
    #     help_text=_("Choose an open source license for your project."),
    #     blank=True,
    #     null=True,
    #     on_delete=models.SET_NULL,
    # )

    funding = models.JSONField(
        verbose_name=_("funding"),
        help_text=_("Include details of any funding recieved for this project."),
        null=True,
        blank=True,
    )

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

    class Meta:
        ordering = (
            "status",
            "-projected_start_date",
        )
        verbose_name = _("project")
        verbose_name_plural = _("projects")

    def __str__(self):
        return force_str(self.title)

    def in_progress(self):
        """Returns True if the project is in progress"""
        return self.status == Project.ProjectStatus.IN_PROGRESS

    def get_contributors(self):
        """Returns all contributors of the project"""
        return None

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"pk": self.pk})

    def get_absolute_url_button(self):
        url = self.get_absolute_url()
        return f'<a href="{url}" class="btn btn-sm btn-primary">View</a>'


class Dataset(models.Model):
    """A dataset is a collection of samples, measurements and associated metadata. The Dataset model
    is the second level model in the Geoluminate schema heirarchy and all geographic sites,
    samples and sample measurements MUST relate back to a dataset."""

    reference = models.OneToOneField(
        "geoluminate_literature.Publication",
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

    name = models.CharField(
        _("name"),
        help_text=_("The name of the dataset."),
        max_length=255,
    )
    description = models.TextField(
        _("description"),
        help_text=_("A description of the dataset and expected outcomes."),
        blank=True,
        null=True,
    )

    projected_start_date = models.DateTimeField(
        _("projected start date"),
        help_text=_("Projected start date of the data collection period."),
        blank=True,
        null=True,
    )
    projected_end_date = models.DateTimeField(
        _("projected end date"),
        help_text=_("Projected end date of the data collection period."),
        blank=True,
        null=True,
    )

    start_date = models.DateTimeField(
        _("start date"),
        help_text=_("Start date of the data collection period."),
        blank=True,
        null=True,
    )
    end_date = models.DateTimeField(
        _("end date"), help_text=_("End date of the data collection period."), blank=True, null=True
    )

    # license = License(
    #     help_text=_("Choose an open source license for your project."),
    #     blank=True,
    #     null=True,
    #     on_delete=models.SET_NULL,
    # )

    class Meta:
        verbose_name = _("dataset")
        verbose_name_plural = _("datasets")

    def get_absolute_url(self):
        return reverse("dataset_detail", kwargs={"pk": self.pk})

    def get_absolute_url_button(self):
        url = self.get_absolute_url()
        return f'<a href="{url}" class="btn btn-sm btn-primary">View</a>'


class Contributor(models.Model):
    """A contributor is a person or organisation that has contributed to the project or
    dataset. This model is based on the Datacite schema for contributors."""

    type = models.CharField(  # noqa: A003
        max_length=255,
        verbose_name=_("contributor type"),
        help_text=_("Contributor type as per the DataCite schema."),
    )
    contributor = models.ForeignKey(
        "user.Profile",
        verbose_name=_("contributor"),
        help_text=_("The person or organisation that contributed to the project or dataset."),
        related_name="contributions",
        on_delete=models.CASCADE,
    )
    dataset = models.ForeignKey(
        Dataset,
        verbose_name=_("dataset"),
        help_text=_("The dataset that this contributor contributed to."),
        related_name="contributors",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("contributor")
        verbose_name_plural = _("contributors")


class Sample(models.Model):
    """This model attempts to roughly replicate the schema of the International
    Generic Sample Number (IGSN) registry. Each sample in this table MUST belong to
    a `geoluminate.contrib.project.models.Dataset`."""

    # can get more info from www.vocabulary.odsm2

    type = models.CharField(
        verbose_name=_("sample type"),
        null=True,
        help_text=_("Specified site name for the related database entry"),
        max_length=255,
    )
    name = models.CharField(
        verbose_name=_("name"),
        null=True,
        help_text=_("Specified site name for the related database entry"),
        max_length=255,
    )
    # description = models.TextField(
    #     _("description"),
    #     help_text=_("A description of the dataset and expected outcomes."),
    #     blank=True,
    #     null=True,
    # )
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

    reused_by = models.ManyToManyField(
        Dataset,
        verbose_name=_("used by"),
        help_text=_("Datasets that make use of this sample but did not collect it."),
        related_name="secondary_samples",
        blank=True,
    )

    _metadata = {
        "title": "name",
        "description": "description",
        "year": "year",
    }

    class Meta:
        verbose_name = _("sample")
        verbose_name_plural = _("generic samples")

    def __unicode__(self):
        return "%s" % (self.name)

    def __str__(self):
        return force_str(self.name) or ""

    def get_absolute_url(self):
        return reverse("sample_detail", kwargs={"pk": self.pk})

    def get_absolute_url_button(self):
        url = self.get_absolute_url()
        return f'<a href="{url}" class="btn btn-sm btn-primary">View</a>'


class Measurement(models.Model):
    class Meta:
        abstract = True

    def get_quality(self):
        """This method should be implemented by classes that subclass this abstract class. It should return a
        value between 0 and 1 that represents the quality of the measurement."""
        raise NotImplementedError
