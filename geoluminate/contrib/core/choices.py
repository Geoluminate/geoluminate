from django.db import models
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _
from research_vocabs.builder.skos import Collection, Concept
from research_vocabs.vocabularies import RemoteVocabulary, VocabularyBuilder


class ProjectDiscoveryTags(VocabularyBuilder):
    LookingForCollaborators = {
        "skos:prefLabel": _("Looking for collaborators"),
        "SKOS.definition": _("This project is actively looking for collaborators to help with the research."),
    }
    LookingForFunding = {
        "skos:prefLabel": _("Looking for funding"),
        "SKOS.definition": _("This project is actively looking for funding to support the research."),
    }

    LookingForInstrumentation = {
        "skos:prefLabel": _("Looking for instrumentation"),
        "SKOS.definition": _(
            "This project is actively looking for scientific instrumentation to support the research."
        ),
    }

    # class Meta:


class ProjectStatus(models.IntegerChoices):
    CONCEPT = 0, _("Concept")
    PLANNING = 1, _("Planning")
    IN_PROGRESS = 2, _("In progress")
    COMPLETE = 3, _("Complete")
    SEARCHING_FOR_COLLABORATORS = 4, _("Unknown")


class ProjectTags(models.TextChoices):
    """A class for storing choices for tags on the Project model."""

    COLLABORATORS_WANTED = "Collaborators wanted", _("Looking for collaborators")
    FUNDING_REQUIRED = "Funding required", _("Looking for funding")
    HAS_FUNDING = "Has funding", _("Has funding")
    POSITIONS_OPEN = "Positions open", _("Positions open")
    EQUIPMENT_REQUIRED = "Equipment required", _("Looking for tools")


# NOTE: These roles attempt to follow the RAiD schema for project roles. However, RAiD specifies both position and role (via CREDiT taxonomy). Our data model only allow for roles, therefore we combien RAid position and role into a single set of choices.


# class ProjectRoles(VocabularyBuilder):
#     PI = {
#         "skos:prefLabel": _("Principal Investigator"),
#         "skos:definition": _("The person who is responsible for the overall scientific leadership of a project."),
#     }
#     COI = {
#         "skos:prefLabel": _("Co-Investigator"),
#         "skos:definition": _("A person who is responsible for a portion of the scientific leadership of a project."),
#     }
#     LEADER = {
#         "skos:prefLabel": _("Leader"),
#         "skos:definition": _("A person who is responsible for the overall leadership of a project."),
#     }
#     CONTACT = {
#         "skos:prefLabel": _("Contact Person"),
#         "skos:definition": _("A person who is responsible for communication about a project."),
#     }


class RAiDPositions(models.TextChoices):
    """A class for storing valid positions for a contributor to a project."""

    PI = "Principal Investigator", _("Principal Investigator")
    COI = "Co-Investigator", _("Co-Investigator")
    LEADER = "Leader", _("Leader")
    CONTACT = "Contact Person", _("Contact Person")
    OTHER = "Other Participant", _("Other Participant")


class RAiDRoles(models.TextChoices):
    """A class for storing valid roles for a contributor to a project."""

    CONCEPTUALIZATION = "Conceptualization", _("Conceptualization")
    DATA_CURATION = "Data Curation", _("Data Curation")
    FORMAL_ANALYSIS = "Formal Analysis", _("Formal Analysis")
    FUNDING_ACQUISITION = "Funding Acquisition", _("Funding Acquisition")
    INVESTIGATION = "Investigation", _("Investigation")
    METHODOLOGY = "Methodology", _("Methodology")
    PROJECT_ADMINISTRATION = "Project Administration", _("Project Administration")
    RESOURCES = "Resources", _("Resources")
    SOFTWARE = "Software", _("Software")
    SUPERVISION = "Supervision", _("Supervision")
    VALIDATION = "Validation", _("Validation")
    VISUALIZATION = "Visualization", _("Visualization")
    WRITING_ORIGINAL_DRAFT = "Writing - Original Draft", _("Writing - Original Draft")
    WRITING_REVIEW_EDITING = "Writing - Review & Editing", _("Writing - Review & Editing")


class DatasetDescriptions(VocabularyBuilder):
    Abstract = Concept(
        prefLabel=_("Abstract"),
        definition=_(
            "A concise summary of a larger work, highlighting main points that allow a reader to quickly understand the essence of the work without reading the entire document."
        ),
    )
    Methods = Concept(
        prefLabel=_("Methods"),
        definition=_("A detailed description of the methods used to collect, process, and analyze the data."),
    )
    SeriesInformation = Concept(
        prefLabel=_("Series Information"),
        definition=_("Information about the series to which the dataset belongs."),
    )
    TableOfContents = Concept(
        prefLabel=_("Table of Contents"),
        definition=_("A list of the contents of the dataset."),
    )
    TechnicalInfo = Concept(
        prefLabel=_("Technical Information"),
        definition=_("Information about the technical aspects of the dataset."),
    )
    Other = Concept(
        prefLabel=_("Other"),
        definition=_("Any other relevant information about the dataset."),
    )

    class Meta:
        name = "dataset-descriptions"
        prefix = "GEOL"
        namespace = "https://www.geoluminate.net/vocabularies/"
        scheme_attrs = {
            "skos:prefLabel": _("Dataset Description Types"),
            "skos:definition": _("Description types for the purpose of metadata archival of datasets."),
        }


class DataciteContributorRoles(VocabularyBuilder):
    CONTACT_PERSON = Concept(
        prefLabel=_("Contact Person"),
        definition=_("The main contact person for the dataset."),
    )
    DATA_COLLECTOR = Concept(
        prefLabel=_("Data Collector"),
        definition=_("The person(s) who collected the data."),
    )
    DATA_CURATOR = Concept(
        prefLabel=_("Data Curator"),
        definition=_("The person(s) who curated the data."),
    )
    DATA_MANAGER = Concept(
        prefLabel=_("Data Manager"),
        definition=_("The person(s) who managed the data."),
    )
    EDITOR = Concept(
        prefLabel=_("Editor"),
        definition=_("The person(s) who edited the data."),
    )
    PRODUCER = Concept(
        prefLabel=_("Producer"),
        definition=_("The person(s) who produced the data."),
    )
    RELATED_PERSON = Concept(
        prefLabel=_("Related Person"),
        definition=_("A person who is related to the dataset."),
    )
    RESEARCHER = Concept(
        prefLabel=_("Researcher"),
        definition=_("The person(s) who conducted the research."),
    )
    PROJECT_LEADER = Concept(
        prefLabel=_("Project Leader"),
        definition=_("The person(s) who led the project."),
    )
    PROJECT_MANAGER = Concept(
        prefLabel=_("Project Manager"),
        definition=_("The person(s) who managed the project."),
    )
    PROJECT_MEMBER = Concept(
        prefLabel=_("Project Member"),
        definition=_("A member of the project."),
    )
    SUPERVISOR = Concept(
        prefLabel=_("Supervisor"),
        definition=_("The person(s) who supervised the project."),
    )
    WORK_PACKAGE_LEADER = Concept(
        prefLabel=_("Work Package Leader"),
        definition=_("The person(s) who led the work package."),
    )
    HOSTING_INSTITUTION = Concept(
        prefLabel=_("Hosting Institution"),
        definition=_("The institution hosting the dataset."),
    )
    RESEARCH_GROUP = Concept(
        prefLabel=_("Research Group"),
        definition=_("The research group associated with the dataset."),
    )
    SPONSOR = Concept(
        prefLabel=_("Sponsor"),
        definition=_("The sponsor of the project."),
    )
    RIGHTS_HOLDER = Concept(
        prefLabel=_("Rights Holder"),
        definition=_("The person(s) who hold the rights to the data."),
    )
    OTHER = Concept(
        prefLabel=_("Other"),
        definition=_("A person who contributed to the dataset in another way."),
    )
    CREATOR = Concept(
        prefLabel=_("Creator"),
        definition=_("The person(s) who created the dataset."),
    )

    class Meta:
        name = "dataset-contributors"
        prefix = "Datacite"
        namespace = "https://www.geoluminate.net/vocabularies/"
        scheme_attrs = {
            "skos:prefLabel": _("Datacite Contributor Roles"),
        }
        collections = {
            "Personal": Collection(
                prefLabel=_("Personal"),
                definition=_("Roles that are related to individuals."),
                ordered=True,
                members=[
                    "ContactPerson",
                    "DataCollector",
                    "DataCurator",
                    "DataManager",
                    "Editor",
                    "Producer",
                    "RelatedPerson",
                    "Researcher",
                    "ProjectLeader",
                    "ProjectManager",
                    "ProjectMember",
                    "Supervisor",
                    "WorkPackageLeader",
                    "RightsHolder",
                    "Other",
                    "Creator",
                ],
            ),
            "Organizational": Collection(
                prefLabel=_("Organizational"),
                definition=_("Roles that are related to organizations."),
                ordered=True,
                members=[
                    "HostingInstitution",
                    "ResearchGroup",
                    "Sponsor",
                    "RightsHolder",
                    "Other",
                ],
            ),
        }


class DataCiteDateTypes(models.TextChoices):
    """DataCite date types as per https://schema.datacite.org/meta/kernel-4.4/doc/DataCite-MetadataKernel_v4.4.pdf#page=46"""

    ACCEPTED = "Accepted", _("Accepted")
    AVAILABLE = "Available", _("Available")
    COPYRIGHTED = "Copyrighted", _("Copyright")
    COLLECTED = "Collected", _("Collected")
    CREATED = "Created", _("Created")
    ISSUED = "Issued", _("Issued")
    SUBMITTED = "Submitted", _("Submitted")
    UPDATED = "Updated", _("Updated")
    VALID = "Valid", _("Valid")
    WITHDRAWN = "Withdrawn", _("Withdrawn")


class DataCiteRelationTypes(models.TextChoices):
    """DataCite relation types as per https://schema.datacite.org/meta/kernel-4.4/doc/DataCite-MetadataKernel_v4.4.pdf#page=58"""

    IsCitedBy = "IsCitedBy", _("Is Cited By")
    Cites = "Cites", _("Cites")
    IsSupplementTo = "IsSupplementTo", _("Is Supplement To")
    IsSupplementedBy = "IsSupplementedBy", _("Is Supplemented By")
    IsContinuedBy = "IsContinuedBy", _("Is Continued By")
    Continues = "Continues", _("Continues")
    Describes = "Describes", _("Describes")
    IsDescribedBy = "IsDescribedBy", _("Is Described By")
    HasMetadata = "HasMetadata", _("Has Metadata")
    IsMetadataFor = "IsMetadataFor", _("Is Metadata For")
    HasVersion = "HasVersion", _("Has Version")
    IsVersionOf = "IsVersionOf", _("Is Version Of")
    IsNewVersionOf = "IsNewVersionOf", _("Is New Version Of")
    IsPreviousVersionOf = "IsPreviousVersionOf", _("Is Previous Version Of")
    IsPartOf = "IsPartOf", _("Is Part Of")
    HasPart = "HasPart", _("Has Part")
    IsPublishedIn = "IsPublishedIn", _("Is Published In")
    IsReferencedBy = "IsReferencedBy", _("Is Referenced By")
    References = "References", _("References")
    IsDocumentedBy = "IsDocumentedBy", _("Is Documented By")
    Documents = "Documents", _("Documents")
    IsCompiledBy = "IsCompiledBy", _("Is Compiled By")
    Compiles = "Compiles", _("Compiles")
    IsVariantFormOf = "IsVariantFormOf", _("Is Variant Form Of")
    IsOriginalFormOf = "IsOriginalFormOf", _("Is Original Form Of")
    IsIdenticalTo = "IsIdenticalTo", _("Is Identical To")
    IsReviewedBy = "IsReviewedBy", _("Is Reviewed By")
    Reviews = "Reviews", _("Reviews")
    IsDerivedFrom = "IsDerivedFrom", _("Is Derived From")
    IsSourceOf = "IsSourceOf", _("Is Source Of")
    IsRequiredBy = "IsRequiredBy", _("Is Required By")
    Requires = "Requires", _("Requires")
    Obsoletes = "Obsoletes", _("Obsoletes")
    IsObsoletedBy = "IsObsoletedBy", _("Is Obsoleted By")


class DataCiteIdentifiers(models.TextChoices):
    """DataCite identifier types as per https://schema.datacite.org/meta/kernel-4.4/doc/DataCite-MetadataKernel_v4.4.pdf#page=54"""

    ARK = "ARK", "ARK"
    ARXIV = "arXiv", "arXiv"
    BIBCODE = "bibcode", "bibcode"
    DOI = "DOI", "DOI"
    EAN13 = "EAN13", "EAN13"
    EISSN = "EISSN", "EISSN"
    HANDLE = "Handle", "Handle"
    IGSN = "IGSN", "IGSN"
    ISBN = "ISBN", "ISBN"
    ISSN = "ISSN", "ISSN"
    ISTC = "ISTC", "ISTC"
    LISSN = "LISSN", "LISSN"
    LSID = "LSID", "LSID"
    PMID = "PMID", "PMID"
    PURL = "PURL", "PURL"
    UPC = "UPC", "UPC"
    URL = "URL", "URL"
    URN = "URN", "URN"


class SampleStatus(RemoteVocabulary):
    class Meta:
        source = {
            "source": "http://vocabulary.odm2.org/api/v1/status/?format=skos",
            "format": "xml",
        }
        prefix = "odm2b"
        namespace = "http://vocabulary.odm2.org/status/"
