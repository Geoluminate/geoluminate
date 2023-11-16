from django.db import models
from django.utils.translation import gettext_lazy as _

# from geoluminate.utils.generic import inherited_choices_factory

# ================== DATACITE ROLES ==================
# https://support.datacite.org/docs/schema-43-attributes#section-contributor
# https://schema.datacite.org/meta/kernel-4.3/doc/DataCite-MetadataKernel_v4.3.pdf

# Datacite treat organisational and personal contributions in the same catergoy which ends up with a messy list of
# options that combines the two. We don't want to present a personal contributor with the option to select
# "HostingInstitution" or "ResearchGroup" as these are organisational roles. To overcome this, we have split the
# Datacite ContributionnType vocabulary into three classes: PersonalRoles, OrganizationalRoles, and OtherRoles.

# Unfortunately, Django choices don't support inheritance, so we have to create a new class that inherits from
# all three classes. This is the ContributionRoles class. Text choices are also created for each class and stored on the
# Contribution model class for easy access in forms.


def inherited_choices_factory(name, *args):
    """Create a TextChoices class from an XMLSchema element."""
    cls_attrs = {}
    for choice_class in args:
        attrs = {a: getattr(choice_class, a) for a in vars(choice_class) if not a.startswith("_")}
        for key, choice in attrs.items():
            cls_attrs[key] = choice.value, choice.label

    return models.TextChoices(f"{name}Choices", cls_attrs)


class PersonalRoles(models.TextChoices):
    """A class for storing choices for ContributionType on the Contribution model. Based on the
    Datacite ContributionType vocabulary."""

    CONTACT_PERSON = "ContactPerson", _("Contact Person")
    DATA_COLLECTOR = "DataCollector", _("Data Collector")
    DATA_CURATOR = "DataCurator", _("Data Curator")
    DATA_MANAGER = "DataManager", _("Data Manager")
    EDITOR = "Editor", _("Editor")
    PRODUCER = "Producer", _("Producer")
    RELATED_PERSON = "RelatedPerson", _("Related Person")
    RESEARCHER = "Researcher", _("Researcher")
    PROJECT_LEADER = "ProjectLeader", _("Project Leader")
    PROJECT_MANAGER = "ProjectManager", _("Project Manager")
    PROJECT_MEMBER = "ProjectMember", _("Project Member")
    SUPERVISOR = "Supervisor", _("Supervisor")
    WORK_PACKAGE_LEADER = "WorkPackageLeader", _("Work Package Leader")


class OrganizationalRoles(models.TextChoices):
    """A class for storing choices for ContributionnnType on the Contribution model. Based on the
    Datacite ContributionType vocabulary."""

    HOSTING_INSTITUTION = "HostingInstitution", _("Hosting Institution")
    RESEARCH_GROUP = "ResearchGroup", _("Research Group")
    SPONSOR = "Sponsor", _("Sponsor")


class OtherRoles(models.TextChoices):
    """A class for storing choices for ContributionType on the Contribution model. Based on the
    Datacite ContributionType vocabulary."""

    RIGHTS_HOLDER = "RightsHolder", _("Rights Holder")
    OTHER = "Other", _("Other")

    # This is specific to the Geoluminate project so that we can distinguish between creators and
    # contributors of a dataset. This is not part of the Datacite ContributionType vocabulary.
    CREATOR = "Creator", _("Creator")

    # DISTRIBUTOR = "Distributor", _("Distributor")


ContributionRoles = inherited_choices_factory("ContributionRole", PersonalRoles, OrganizationalRoles, OtherRoles)
