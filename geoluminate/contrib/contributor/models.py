import json

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models as django_models
from django.db.models import CharField, F, Value
from django.db.models.functions import Concat
from django.templatetags.static import static
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from multiselectfield.utils import get_max_length
from taggit.managers import TaggableManager

from geoluminate import models
from geoluminate.contrib.core.models import Dataset, Project, Sample

from . import choices
from .managers import ContributionManager


class Identifier(models.Model):
    """A model for storing identifiers for users and organisations."""

    user = models.ForeignKey("contributor.Contributor", related_name="identifiers", on_delete=models.CASCADE)
    identifier = models.CharField(max_length=255, verbose_name=_("identifier"))
    scheme = models.CharField(max_length=255, verbose_name=_("scheme"))
    url = models.URLField(verbose_name="URL", blank=True, null=True)

    def __str__(self):
        return self.identifier


class Contributor(models.Model):
    """A Contributor is a person or organisation that makes a contribution to a project, dataset, sample or measurement
    within the database. This model stores publicly available information about the contributor that can be used
    for proper attribution and formal publication of datasets. The fields are designed to align with the DataCite
    Contributor schema."""

    image = models.ImageField(
        upload_to="profile_images/",
        verbose_name=_("profile image"),
        help_text=_("A profile image for the contributor."),
        blank=True,
        null=True,
    )

    name = models.CharField(
        max_length=512,
        verbose_name=_("display name"),
        help_text=_("This name is displayed publicly within the website."),
    )

    about = models.TextField(null=True, blank=True)

    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    interests = TaggableManager(
        _("interests"), help_text=_("A list of research interests for the contributor."), blank=True
    )

    lang = models.CharField(
        max_length=255,
        verbose_name=_("language"),
        help_text=_("Language of the contributor."),
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("contributor")
        verbose_name_plural = _("contributors")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("contributor:detail", kwargs={"pk": self.pk})

    @property
    def type(self):
        if self.user:
            return "Person"
        else:
            return "Organization"

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

    @property
    def datasets(self):
        return Contribution.objects.filter(
            profile=self,
            content_type=ContentType.objects.get_for_model(Dataset),
        ).all()

    @property
    def projects(self):
        return Contribution.objects.filter(
            profile=self,
            content_type=ContentType.objects.get_for_model(Project),
        ).all()

    @property
    def samples(self):
        return Contribution.objects.filter(
            profile=self,
            content_type=ContentType.objects.get_for_model(Sample),
        ).all()

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
            .annotate(id=models.F("profile__id"), label=models.F("profile__name"), image=models.F("profile__image"))
            .values("id", "label", "object_id", "image")
        )

        full_name = Concat(
            F("model__user_first_name"), Value(" "), F("model__user_last_name"), output_field=CharField()
        )

        # get unique contributors and count the number of times they appear in the queryset
        nodes_qs = data.values("id", "label", "image").annotate(value=models.Count("id")).distinct()

        nodes = []
        for d in nodes_qs:
            if d["image"]:
                d["image"] = settings.MEDIA_URL + d["image"]
            nodes.append(d)

        print("Nodes: ", nodes)

        object_ids = set([d["object_id"] for d in data])

        edges = []
        for obj in object_ids:
            ids = list(set([i["id"] for i in data if i["object_id"] == obj]))

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

    roles = models.MultiSelectField(
        choices=CONTRIBUTOR_ROLES.choices,
        max_length=get_max_length(CONTRIBUTOR_ROLES.choices, None),
        verbose_name=_("roles"),
        help_text=_("Contribution roles as per the Datacite ContributionType vocabulary."),
    )
    profile = models.ForeignKey(
        "contributor.Contributor",
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
