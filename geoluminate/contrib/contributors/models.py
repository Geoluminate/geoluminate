import random

from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count
from django.templatetags.static import static
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from jsonfield_toolkit.models import ArrayField
from polymorphic.models import PolymorphicModel

# from django.db.models.fields.files import FieldFile
from geoluminate.core.models import AbstractIdentifier, PolymorphicMixin
from geoluminate.core.utils import inherited_choices_factory
from geoluminate.db import models

from . import choices
from .managers import UserManager


def profile_image_path(instance, filename):
    """Return the path to the profile image for a contributor."""
    return f"contributors/{instance.pk}.{filename.split('.')[-1]}"


class Contributor(models.Model, PolymorphicMixin, PolymorphicModel):
    """A Contributor is a person or organisation that makes a contribution to a project, dataset, sample or measurement
    within the database. This model stores publicly available information about the contributor that can be used
    for proper attribution and formal publication of datasets. The fields are designed to align with the DataCite
    Contributor schema."""

    image = ThumbnailerImageField(
        verbose_name=_("profile image"),
        resize_source={"size": (1200, 1200)},
        # processors=[SmartResize(600, 600)],
        # options={"quality": 60},
        blank=True,
        null=True,
        upload_to=profile_image_path,
    )

    name = models.CharField(
        max_length=512,
        verbose_name=_("preferred name"),
        # help_text=_("This name is displayed publicly within the website."),
    )

    alternative_names = models.JSONField(
        verbose_name=_("alternative names"),
        help_text=_("Any other names by which the contributor is known."),
        null=True,
        blank=True,
        default=list,
    )

    profile = models.TextField(_("profile"), null=True, blank=True)

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

    def default_affiliation(self):
        """Returns the default affiliation for the contributor. TODO: make this a foreign key to an organization model."""
        if self.user:
            return self.user.organizations_organization.first()
        return None

    def location(self):
        """Returns the location of the contributor. TODO: make this a foreign key to a location model."""
        return random.choice(["Potsdam", "Adelaide", "Dresden"])
        if self.user:
            return self.user.organization.location
        return None

    def get_absolute_url(self):
        return reverse("contributor-detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("contributor-update", kwargs={"pk": self.pk})

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

    @cached_property
    def owner(self):
        return self.user or self.organization

    @property
    def preferred_email(self):
        if self.user:
            return self.user.email
        return self.organization.owner.user.email


class Person(AbstractUser, Contributor):
    objects = UserManager()  # type: ignore[var-annotated]

    email = models.EmailField(_("email address"), unique=True)

    # settings = models.JSONField(default=dict, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    username = Contributor.__str__
    # polymorphic_primary_key_name = "id"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.name = f"{self.first_name} {self.last_name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_provider(self, provider: str):
        qs = self.socialaccount_set.filter(provider=provider)  # type: ignore[attr-defined]
        return qs.get() if qs else None


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

    class Meta:
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("organization-detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("organization-update", kwargs={"pk": self.pk})

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


class Identifier(AbstractIdentifier):
    IdentifierLookup = choices.IdentifierLookup
    PERS_ID_TYPES = choices.PersonalIdentifiers
    ORG_ID_TYPES = choices.OrganizationalIdentifiers
    SCHEME_CHOICES = inherited_choices_factory("ContributorIdentifiers", PERS_ID_TYPES, ORG_ID_TYPES)
    scheme = models.CharField(_("scheme"), max_length=32, choices=SCHEME_CHOICES)
    object = models.ForeignKey(to=Contributor, on_delete=models.CASCADE)


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
