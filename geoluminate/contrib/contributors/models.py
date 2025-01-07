import random

from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Count
from django.templatetags.static import static
from django.urls import reverse

# from rest_framework.authtoken.models import Token
from django.utils.encoding import force_str
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from jsonfield_toolkit.models import ArrayField
from polymorphic.models import PolymorphicModel
from shortuuid.django_fields import ShortUUIDField

from geoluminate.contrib.contributors.managers import ContributionManager
from geoluminate.contrib.generic.models import GenericModel, Identifier

# from django.db.models.fields.files import FieldFile
from geoluminate.core.models import PolymorphicMixin
from geoluminate.core.utils import default_image_path

from .managers import UserManager


def contributor_permissions_default():
    return {"edit": False}


class Contributor(PolymorphicMixin, PolymorphicModel):
    """A Contributor is a person or organisation that makes a contribution to a project, dataset, sample or measurement
    within the database. This model stores publicly available information about the contributor that can be used
    for proper attribution and formal publication of datasets. The fields are designed to align with the DataCite
    Contributor schema."""

    id = ShortUUIDField(
        editable=False,
        unique=True,
        prefix="c",
        verbose_name="UUID",
        primary_key=True,
    )

    image = ThumbnailerImageField(
        verbose_name=_("profile image"),
        blank=True,
        null=True,
        upload_to=default_image_path,
    )

    name = models.CharField(
        max_length=512,
        verbose_name=_("preferred name"),
        # help_text=_("This name is displayed publicly within the website."),
    )

    alternative_names = ArrayField(
        base_field=models.CharField(max_length=255),
        verbose_name=_("alternative names"),
        help_text=_("Any other names by which the contributor is known."),
        null=True,
        blank=True,
        default=list,
    )

    profile = models.TextField(_("profile"), null=True, blank=True)
    identifiers = GenericRelation("generic.Identifier")

    # interests = TaggableConcepts(
    #     verbose_name=_("research interests"),
    #     help_text=_("A list of research interests for the contributor."),
    #     blank=True,
    # )

    links = ArrayField(
        base_field=models.URLField(),
        verbose_name=_("links"),
        help_text=_("A list of online resources related to this contributor."),
        null=True,
        blank=True,
        default=list,
    )

    lang = ArrayField(
        base_field=models.CharField(max_length=5),
        verbose_name=_("language"),
        help_text=_("Language of the contributor."),
        blank=True,
        null=True,
        default=list,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("contributor")
        verbose_name_plural = _("contributors")

    @staticmethod
    def base_class():
        # this is required for many of the class methods in PolymorphicMixin
        return Contributor

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("person-detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("contributor-update", kwargs={"pk": self.pk})

    def profile_image(self):
        if self.image:
            return self.image.url
        return static("img/brand/icon.svg")

    def type(self):
        return self.polymorphic_ctype.model
        # if hasattr(self, "person", None):
        #     return "person"
        # return "organization"

    @property
    def projects(self):
        Project = apps.get_model("fairdm.Project")
        return Project.objects.filter(contributors__contributor=self)

    @property
    def datasets(self):
        Dataset = apps.get_model("fairdm.Dataset")
        return Dataset.objects.filter(contributors__contributor=self)

    @property
    def samples(self):
        Sample = apps.get_model("fairdm.Sample")
        return Sample.objects.filter(contributors__contributor=self)

    @property
    def measurements(self):
        Measurement = apps.get_model("fairdm.Measurement")
        return Measurement.objects.filter(contributors__contributor=self)


class Person(AbstractUser, Contributor):
    objects = UserManager()  # type: ignore[var-annotated]

    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    username = Contributor.__str__
    # polymorphic_primary_key_name = "id"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk and not self.name:
            self.name = f"{self.first_name} {self.last_name}"
        super().save(*args, **kwargs)

    def get_provider(self, provider: str):
        qs = self.socialaccount_set.filter(provider=provider)  # type: ignore[attr-defined]
        return qs.get() if qs else None

    def default_affiliation(self):
        """Returns the default affiliation for the contributor. TODO: make this a foreign key to an organization model."""
        if self.user:
            return self.user.organizations_organization.first()
        return None

    def location(self):
        """Returns the location of the contributor. TODO: make this a foreign key to a location model."""
        return random.choice(["Potsdam", "Adelaide", "Dresden"])
        return self.organization.location

    def get_absolute_url(self):
        return reverse("contributor-detail", kwargs={"pk": self.pk})

    @property
    def given(self):
        """Alias for self.first_name."""
        return self.first_name

    @property
    def family(self):
        """Alias for self.last_name."""
        return self.last_name

    def orcid_data(self):
        """Returns the ORCID data for the user if available."""
        orcid = self.get_provider("orcid")
        if orcid:
            return orcid.extra_data
        return None


class OrganizationMember(models.Model):
    """A membership model that links a person to an organization."""

    class MembershipType(models.IntegerChoices):
        MEMBER = 1, _("Member")
        ADMIN = 2, _("Admin")
        OWNER = 3, _("Owner")

    person = models.ForeignKey(
        to="contributors.Person",
        on_delete=models.CASCADE,
        related_name="organization_memberships",
        verbose_name=_("person"),
        help_text=_("The person that is a member of the organization."),
    )

    organization = models.ForeignKey(
        to="contributors.Organization",
        on_delete=models.CASCADE,
        related_name="memberships",
        verbose_name=_("organization"),
        help_text=_("The organization that the person is a member of."),
    )
    type = models.IntegerField(
        _("type"),
        choices=MembershipType,
        default=MembershipType.MEMBER,
        help_text=_("The type of membership that the person has with the organization"),
    )

    class Meta:
        verbose_name = _("organization membership")
        verbose_name_plural = _("organization memberships")

    def __str__(self):
        return f"{self.person} - {self.organization}"


class Organization(Contributor):
    """An organization is a contributor that represents a group of people, such as a university, research institute,
    company or government agency. Organizations can have multiple members and can be affiliated with other organizations.
    Organizations can also have sub-organizations, such as departments or research groups."""

    members = models.ManyToManyField(
        to="contributors.Person",
        through="contributors.OrganizationMember",
        verbose_name=_("members"),
        related_name="affiliations",
        help_text=_("A list of personal contributors that are members of the organization."),
    )

    parent = models.ForeignKey(
        to="self",
        on_delete=models.CASCADE,
        related_name="sub_organizations",
        verbose_name=_("parent organization"),
        help_text=_("The organization that this organization is a part of."),
        blank=True,
        null=True,
    )

    ror = models.JSONField(
        verbose_name=_("Research Organization Registry"),
        help_text=_("A JSON object containing information about the organization from the ROR API."),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")

    def __str__(self):
        return self.name

    @classmethod
    def from_ror(self, data):
        """Create an organization from a ROR ID."""
        ror_id = Identifier.objects.filter(scheme="ror", identifier=data["id"]).first()
        if ror_id:
            return ror_id.object

        instance = Organization.objects.create(
            name=data["name"],
            alternative_names=[*data.get("aliases", []), *data.get("acronyms", [])],
            ror=data,
            links=data.get("links", []),
        )

        Identifier.objects.create(
            scheme="ror",
            identifier=data["id"],
            object=instance,
        )
        return instance

    # @property
    # def type(self):
    #     return _("Organizational")

    # @property
    # def given(self):
    #     return ""

    # @property
    # def family(self):
    #     return ""

    # @property
    # def owner(self):
    #     return self.owner

    # @property
    # def preferred_email(self):
    #     return self.owner.email


class Contribution(GenericModel):
    """A contributor is a person or organisation that has contributed to the project or
    dataset. This model is based on the Datacite schema for contributors."""

    objects = ContributionManager().as_manager()

    contributor = models.ForeignKey(
        "contributors.Contributor",
        verbose_name=_("contributor"),
        help_text=_("The person or organisation that contributed to the project or dataset."),
        related_name="contributions",
        null=True,
        on_delete=models.SET_NULL,
    )

    roles = models.JSONField(
        verbose_name=_("roles"),
        help_text=_("Assigned roles for this contributor."),
        default=list,
        null=True,
        blank=True,
    )

    # we can't rely on the contributor field to store necessary information, as the profile may have changed or been deleted, therefore we need to store the contributor's name and other details at the time of publication
    store = models.JSONField(
        _("contributor"),
        help_text=_("A JSON representation of the contributor profile at the time of publication"),
        default=dict,
    )

    # holds the permissions for each contributor, e.g. whether they can edit the object
    permissions = models.JSONField(
        _("permissions"),
        help_text=_("A JSON representation of the contributor's permissions at the time of publication"),
        default=contributor_permissions_default,
    )

    class Meta:
        verbose_name = _("contributor")
        verbose_name_plural = _("contributors")
        unique_together = ("content_type", "object_id", "contributor")

    def __str__(self):
        return force_str(self.contributor)

    def __repr__(self):
        return f"<{self.contributor}: {self.roles}>"

    def get_absolute_url(self):
        """Returns the absolute url of the contributor's profile."""
        return self.contributor.get_absolute_url()

    def get_update_url(self):
        related_name = self.object._meta.model_name
        letter = related_name[0]
        return reverse("contribution-update", kwargs={"pk": self.object.pk, "model": letter})

    def get_create_url(self):
        related_name = self.object._meta.model_name
        letter = related_name[0]
        return reverse("contribution-create", kwargs={"model": letter, "pk": self.object.pk})

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


def forwards():
    EmailAddress = apps.get_model("account.EmailAddress")
    User = apps.get_model(settings.AUTH_USER_MODEL)
    user_email_field = getattr(settings, "ACCOUNT_USER_MODEL_EMAIL_FIELD", "email")

    def get_users_with_multiple_primary_email():
        user_pks = []
        for email_address_dict in (
            EmailAddress.objects.filter(primary=True).values("user").annotate(Count("user")).filter(user__count__gt=1)
        ):
            user_pks.append(email_address_dict["user"])
        return User.objects.filter(pk__in=user_pks)

    def unset_extra_primary_emails(user):
        qs = EmailAddress.objects.filter(user=user, primary=True)
        primary_email_addresses = list(qs)
        if not primary_email_addresses:
            return
        primary_email_address = primary_email_addresses[0]
        if user_email_field:
            for address in primary_email_addresses:
                if address.email.lower() == getattr(user, user_email_field, "").lower():
                    primary_email_address = address
                    break
        qs.exclude(pk=primary_email_address.pk).update(primary=False)

    for user in get_users_with_multiple_primary_email().iterator():
        unset_extra_primary_emails(user)
