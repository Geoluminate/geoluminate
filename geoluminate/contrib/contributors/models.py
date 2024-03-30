import json
import random

from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.db import models as django_models
from django.db.models import Case, CharField, F, IntegerField, Value, When
from django.db.models.functions import Concat
from django.templatetags.static import static
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from research_vocabs.fields import TaggableConcepts

from geoluminate.contrib.datasets.models import Dataset
from geoluminate.contrib.projects.models import Project
from geoluminate.contrib.reviews.models import Review
from geoluminate.contrib.samples.models import Sample
from geoluminate.db import models

# from geoluminate.models import Dataset, Project, Review, Sample
from . import choices
from .managers import ContributionManager, ContributorManager, OrganizationManager, PersonManager


class Contributor(models.Model):
    """A Contributor is a person or organisation that makes a contribution to a project, dataset, sample or measurement
    within the database. This model stores publicly available information about the contributor that can be used
    for proper attribution and formal publication of datasets. The fields are designed to align with the DataCite
    Contributor schema."""

    objects = ContributorManager().as_manager()

    image = models.ImageField(
        upload_to="profile_images/",
        verbose_name=_("profile image"),
        blank=True,
        null=True,
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="profile",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    organization = models.OneToOneField(
        "organizations.Organization",
        related_name="profile",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=512,
        verbose_name=_("display name"),
        help_text=_("This name is displayed publicly within the website."),
    )

    about = models.TextField(null=True, blank=True)

    interests = TaggableConcepts(
        verbose_name=_("research interests"),
        help_text=_("A list of research interests for the contributor."),
        blank=True,
    )

    lang = models.CharField(
        max_length=255,
        verbose_name=_("language"),
        help_text=_("Language of the contributor."),
        blank=True,
        null=True,
    )

    identifiers = models.ManyToManyField(
        "core.Identifier",
        verbose_name=_("identifiers"),
        help_text=_("A list of identifiers for the contributor."),
        blank=True,
    )

    # preferred_lang = models.CharField(
    #     max_length=255,
    #     verbose_name=_("preferred language"),
    #     help_text=_("Language of the contributor."),
    #     blank=True,
    #     null=True,
    # )

    class Meta:
        ordering = ["name"]
        verbose_name = _("contributor")
        verbose_name_plural = _("contributors")

    def __str__(self):
        return self.name

    def default_affiliation(self):
        """Returns the default affiliation for the contributor. TODO: make this a foreign key to an organization model."""
        if self.user:
            return self.user.organizations_organization.first()
        return None

    def location(self):
        """Returns the location of the contributor. TODO: make this a foreign key to a location model."""
        return random.choice(["Potsdam", "Adelaide", "Dresden"])  # noqa: S311
        if self.user:
            return self.user.organization.location
        return None

    def get_absolute_url(self):
        return reverse("contributor:detail", kwargs={"uuid": self.uuid})

    def profile_image(self):
        if self.image:
            return self.image.url
        return static("img/brand/icon.svg")

    @property
    def type(self):
        if self.user:
            return _("Personal")
        return _("Organizational")

    @property
    def given(self):
        if self.user:
            return self.user.first_name
        return ""

    @property
    def family(self):
        if self.user:
            return self.user.last_name
        return ""

    @classmethod
    def get_contribution_by_type(cls, model):
        if isinstance(model, str):
            model = apps.get_model(model)
        return Case(
            When(
                contributions__content_type=ContentType.objects.get_for_model(model),
                then=1,
            ),
            output_field=IntegerField(),
        )

    @property
    def datasets(self):
        return Dataset.objects.filter(
            contributors__profile=self,
        )

    @property
    def projects(self):
        return Project.objects.filter(
            contributors__profile=self,
        )
        # return Contribution.objects.filter(
        #     profile=self,
        #     content_type=ContentType.objects.get_for_model(Project),
        # )

    @property
    def samples(self):
        return Contribution.objects.filter(
            profile=self,
            content_type=ContentType.objects.get_for_model(Sample),
        )

    @property
    def reviews(self):
        if self.user:
            return self.user.review_set.all()
        # return an empty Review queryset
        return Review.objects.none()

    def get_related_contributions(self):
        """Returns a queryset of all contributions related to datasets contributed to by the current contributor."""

        dataset_ids = self.contributions.filter(
            content_type=ContentType.objects.get_for_model(Dataset),
        ).values_list("object_id", flat=True)

        return Contribution.objects.filter(object_id__in=dataset_ids)

    def get_network(self):
        # get list of content_types that the contributor has contributed to
        object_ids = self.contributions.values_list("object_id", flat=True)

        # get all contributions to those content_types
        data = (
            self.get_related_contributions()
            .values("profile", "object_id")
            .annotate(
                id=models.F("profile__id"),
                label=models.F("profile__name"),
                image=models.F("profile__image"),
            )
            .values("id", "label", "object_id", "image")
        )

        Concat(
            F("model__user_first_name"),
            Value(" "),
            F("model__user_last_name"),
            output_field=CharField(),
        )

        # get unique contributors and count the number of times they appear in the queryset
        nodes_qs = data.values("id", "label", "image").annotate(value=models.Count("id")).distinct()

        nodes = []
        for d in nodes_qs:
            if d["image"]:
                d["image"] = settings.MEDIA_URL + d["image"]
            nodes.append(d)

        print("Nodes: ", nodes)

        object_ids = {d["object_id"] for d in data}

        edges = []
        for obj in object_ids:
            ids = list({i["id"] for i in data if i["object_id"] == obj})

            ids.sort()

            # get list of unique id pairs
            pairs = []
            for i in range(len(ids)):
                for j in range(i + 1, len(ids)):
                    pairs.append((ids[i], ids[j]))

            edges += pairs

        # count the number of times each pair appears in edges
        edges = [{"from": f, "to": t, "value": edges.count((f, t))} for f, t in set(edges)]

        vis_js = {"nodes": list(nodes), "edges": edges}
        print(edges)
        # serialize nodes queryset to json

        return json.dumps(vis_js)

    @cached_property
    def owner(self):
        if self.user:
            return self.user
        return self.organization

    @property
    def preferred_email(self):
        if self.user:
            return self.user.email
        return self.organization.owner.user.email

    # def is_active(self):
    # """Returns True if the contributor is listed on a dataset that has been accepted in the past"""


class PersonalContributor(Contributor):
    objects = PersonManager()

    class Meta:
        proxy = True
        verbose_name = _("person")
        verbose_name_plural = _("people")


class OrganizationalContributor(Contributor):
    objects = OrganizationManager()

    class Meta:
        proxy = True
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")


class Contribution(django_models.Model):
    """A contributor is a person or organisation that has contributed to the project or
    dataset. This model is based on the Datacite schema for contributors."""

    objects = ContributionManager().as_manager()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    CONTRIBUTOR_ROLES = choices.ContributionRoles
    PERSONAL_ROLES = choices.PersonalRoles
    ORGANIZATIONAL_ROLES = choices.OrganizationalRoles
    OTHER_ROLES = choices.OtherRoles

    roles = ArrayField(
        models.CharField(
            max_length=len(max(CONTRIBUTOR_ROLES.values, key=len)),
            choices=CONTRIBUTOR_ROLES.choices,
            # verbose_name=_("roles"),
            # help_text=_("Contribution roles as per the Datacite ContributionType vocabulary."),
        ),
        verbose_name=_("roles"),
        help_text=_("Assigned roles for this contributor."),
        size=len(CONTRIBUTOR_ROLES.choices),
    )
    profile = models.ForeignKey(
        "contributors.Contributor",
        verbose_name=_("contributor"),
        help_text=_("The person or organisation that contributed to the project or dataset."),
        related_name="contributions",
        null=True,
        on_delete=models.SET_NULL,
    )
    contributor = models.JSONField(
        _("contributor"),
        help_text=_("A JSON representation of the contributor profile at the time of publication"),
        default=dict,
    )

    class Meta:
        verbose_name = _("contribution")
        verbose_name_plural = _("contributions")
        unique_together = ("profile", "content_type", "object_id")
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def save(self, *args, **kwargs):
        """Either data or a profile should be passed to the constructor. If data is passed, search the obect for an ORCID and try to find an existing profile. If no profile is found, create a new one. If a profile is passed, use that profile to create a data object."""
        # if not self.pk:
        #     # if data is passed to constructor on creation, set the profile field to the data
        #     if self.contributor and not self.profile:
        #         self.profile = utils.csljson_to_contributor(self.contributor)
        #     elif self.profile and not self.contributor:
        #         self.contributor = utils.csljson_from_contributor(self.profile)

        super().save(*args, **kwargs)

    def __str__(self):
        return force_str(self.profile)

    def get_absolute_url(self):
        """Returns the absolute url of the contributor's profile."""
        return self.profile.get_absolute_url()

    def profile_to_data(self):
        """Converts the profile to a JSON object."""

        data = {
            "name": self.profile.name,
            "given": self.profile.given,
            "family": self.profile.family,
        }

        ORCID = self.profile.identifiers.filter(scheme="ORCID").first()
        if ORCID:
            data["ORCID"] = ORCID.identifier

        affiliation = self.profile.default_affiliation()
        if affiliation:
            data["affiliation"] = affiliation

        return data
