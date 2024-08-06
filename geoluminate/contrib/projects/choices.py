from django.db import models
from django.utils.translation import gettext_lazy as _
from research_vocabs.builder.skos import Concept
from research_vocabs.vocabularies import VocabularyBuilder


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


# class ProjectDescriptions(models.TextChoices):
#     """A class for storing choices for descriptions on the Project model."""

#     ABSTRACT = "Abstract", _("Abstract")
#     INTRODUCTION = "Introduction", _("Introduction")
#     BACKGROUND = "Background", _("Background")
#     OBJECTIVES = "Objectives", _("Objectives")
#     OUTPUT = "ExpectedOutput", _("Expected Output")
#     METHODS = "Methods", _("Methods")
#     CONCLUSIONS = "Conclusions", _("Conclusions")
#     OTHER = "Other", _("Other")


class ProjectDescriptions(VocabularyBuilder):
    Abstract = Concept(
        prefLabel=_("Abstract"),
        definition=_(
            "A concise summary of a larger work, highlighting main points that allow a reader to quickly understand the essence of the work without reading the entire document."
        ),
    )
    # Abstract = {
    #     "skos:prefLabel": _("Abstract"),
    #     "skos:definition": _(
    #         "A concise summary of a larger work, highlighting main points that allow a reader to quickly understand the essence of the work without reading the entire document."
    #     ),
    # }
    # TODO: finsih this from above...

    class Meta:
        name = "project-descriptions"
        prefix = "GEOL"
        namespace = "https://www.geoluminate.net/vocabularies/"
        scheme_attrs = {
            "skos:prefLabel": _("Project Description Types"),
            "skos:definition": _("Description types for the purpose of metadata archival of research projects."),
        }


class ProjectDates(VocabularyBuilder):
    StartDate = {
        "skos:prefLabel": _("Start Date"),
        "skos:definition": _("The official start date of the project."),
    }
    EndDate = {
        "skos:prefLabel": _("End Date"),
        "skos:definition": _("The official end date of the project."),
    }

    class Meta:
        name = "project-dates"
        prefix = "GEOL"
        namespace = "https://www.geoluminate.net/vocabularies/"
        scheme_attrs = {
            "skos:prefLabel": _("Project Date Types"),
            "skos:definition": _("Important dates regarding archival of metadata related to project management."),
        }


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
