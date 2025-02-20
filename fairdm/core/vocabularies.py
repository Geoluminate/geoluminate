from django.utils.translation import gettext_lazy as _
from research_vocabs.builder.skos import Collection, Concept
from research_vocabs.vocabularies import VocabularyBuilder


class FairDMIdentifiers(VocabularyBuilder):
    ORCID = {
        "skos:prefLabel": _("ORCID iD"),
        "skos:definition": _(
            "A persistent digital identifier that uniquely identifies researchers and scholars, ensuring correct attribution of their work."
        ),
        "dcterms:source": "http://orcid.org/",
    }

    RESEARCHER_ID = {
        "skos:prefLabel": _("ResearcherID"),
        "skos:definition": _("An identifier assigned to researchers by Web of Science to track author publications."),
        "dcterms:source": "https://www.researcherid.com/",
    }

    ROR = {
        "skos:prefLabel": _("ROR"),
        "skos:definition": _(
            "A unique identifier for research organizations, provided by the Research Organization Registry (ROR)."
        ),
        "dcterms:source": "https://ror.org/",
    }

    # No longer used.
    # GRID = {
    #     "skos:prefLabel": _("GRID"),
    #     "skos:definition": _(
    #         "A global database of research institution identifiers, now succeeded by ROR."
    #     ),
    #     "dcterms:source": "https://www.grid.ac/",
    # }

    WIKIDATA = {
        "skos:prefLabel": _("Wikidata"),
        "skos:definition": _(
            "A free and open knowledge base that provides structured data, including identifiers for people, organizations, and concepts."
        ),
        "dcterms:source": "https://www.wikidata.org/",
    }

    ISNI = {
        "skos:prefLabel": _("ISNI"),
        "skos:definition": _(
            "An International Standard Name Identifier (ISNI) used to uniquely identify individuals and organizations involved in creative activities."
        ),
        "dcterms:source": "https://www.isni.org/",
    }

    CROSSREF_FUNDER_ID = {
        "skos:prefLabel": _("Crossref Funder ID"),
        "skos:definition": _("An identifier assigned by Crossref to uniquely identify funding organizations."),
        "dcterms:source": "https://www.crossref.org/fundingdata/",
    }

    class Meta:
        name = "fairdm-descriptions"
        prefix = "FAIRDM"
        namespace = "https://www.fairdm.net/vocabularies/"
        scheme_attrs = {
            "skos:prefLabel": _("FairDM Identifiers"),
            "skos:definition": _("Identifiers for the purpose of metadata archival of research projects."),
        }


class FairDMDescriptions(VocabularyBuilder):
    Abstract = Concept(
        prefLabel=_("Abstract"),
        definition=_(
            "An abstract is a brief, high-level summary that describes the dataset’s purpose, scope, key content, and relevance. It provides an overview of what the dataset contains and why it is important, helping potential users assess its applicability to their research."
        ),
    )

    Methods = Concept(
        prefLabel=_("Methods"),
        definition=_(
            "A detailed description of the methodologies used to collect, process, and analyze the dataset. This may include data collection techniques, instrumentation, sampling strategies, processing workflows, and software used."
        ),
    )

    SeriesInformation = Concept(
        prefLabel=_("Series Information"),
        definition=_(
            "Information about the dataset’s relationship to a series of datasets or a broader collection. This may include volume or issue numbers, hierarchical relationships, or references to a parent dataset."
        ),
    )

    TechnicalInfo = Concept(
        prefLabel=_("Technical Information"),
        definition=_(
            "Details about the dataset’s technical specifications, including file formats, data structures, encoding standards, storage requirements, and any dependencies on specific software or hardware."
        ),
    )
    Introduction = Concept(
        prefLabel=_("Introduction"),
        definition=_("The opening section of a research article, thesis, or proposal."),
    )

    Background = Concept(
        prefLabel=_("Background"),
        definition=_("The context in which the research was conducted."),
    )

    Objectives = Concept(
        prefLabel=_("Objectives"),
        definition=_("The goals of the research project."),
    )

    ExpectedOutput = Concept(
        prefLabel=_("Expected Output"),
        definition=_("The anticipated results of the research project."),
    )

    Conclusions = Concept(
        prefLabel=_("Conclusions"),
        definition=_("The final thoughts and findings of the research."),
    )

    Other = Concept(
        prefLabel=_("Other"),
        definition=_("Any additional descriptive information that does not fit into the defined categories."),
    )

    SampleCollection = {
        "skos:prefLabel": _("Collection"),
        "skos:definition": _("The process of collecting a sample."),
    }

    SamplePreparation = {
        "skos:prefLabel": _("Preparation"),
        "skos:definition": _("The process of preparing a sample for analysis."),
    }

    SampleStorage = {
        "skos:prefLabel": _("Storage"),
        "skos:definition": _("The process of storing a sample."),
    }

    SampleDestruction = {
        "skos:prefLabel": _("Destruction"),
        "skos:definition": _("The process of destroying a sample."),
    }

    MeasurementConditions = Concept(
        prefLabel=_("Conditions"),
        definition=_(
            "The specific environmental or situational factors present during the measurement process, which can influence or affect the outcome."
        ),
    )

    MeasurementSetup = Concept(
        prefLabel=_("Preparation"),
        definition=_(
            "The set of procedures and steps executed prior to conducting a measurement, ensuring accuracy, reliability, and consistency in the results obtained."
        ),
    )

    MeasurementTearDown = Concept(
        prefLabel=_("Tear Down"),
        definition=_(
            "The set of procedures and steps executed after conducting a measurement, ensuring that all equipment is properly cleaned, stored, or maintained for future use."
        ),
    )

    class Meta:
        name = "fairdm-descriptions"
        prefix = "FAIRDM"
        namespace = "https://www.fairdm.net/vocabularies/"
        scheme_attrs = {
            "skos:prefLabel": _("FairDM Descriptions"),
            "skos:definition": _("Description types for the purpose of metadata archival of research projects."),
        }
        collections = {
            "Project": Collection(
                prefLabel=_("Project Descriptions"),
                definition=_("Description types for the purpose of metadata archival of research projects."),
                ordered=True,
                members=[
                    "Abstract",
                    "Introduction",
                    "Background",
                    "Objectives",
                    "ExpectedOutput",
                    "Methods",
                    "Conclusions",
                    "Other",
                ],
            ),
            "Dataset": Collection(
                prefLabel=_("Dataset Descriptions"),
                definition=_("Description types for the purpose of metadata archival of research datasets."),
                ordered=True,
                members=[
                    "Abstract",
                    "Methods",
                    "SeriesInformation",
                    "TechnicalInfo",
                    "Other",
                ],
            ),
            "Sample": Collection(
                prefLabel=_("Sample Descriptions"),
                definition=_("Description types for the purpose of metadata archival of research samples."),
                ordered=True,
                members=[
                    "SampleCollection",
                    "SamplePreparation",
                    "SampleStorage",
                    "SampleDestruction",
                    "Other",
                ],
            ),
            "Measurement": Collection(
                prefLabel=_("Measurement Descriptions"),
                definition=_("Description types for the purpose of metadata archival of research measurements."),
                ordered=True,
                members=[
                    "MeasurementConditions",
                    "MeasurementPreparation",
                    "MeasurementTearDown",
                    "Other",
                ],
            ),
        }


class FairDMDates(VocabularyBuilder):
    Available = {
        "skos:prefLabel": _("Date Available"),
        "skos:definition": _("The date on which the dataset becomes available to the public."),
    }

    CollectionStart = {
        "skos:prefLabel": _("Collection Start Date"),
        "skos:definition": _("The date on which the data collection process began."),
    }

    CollectionEnd = {
        "skos:prefLabel": _("Collection End Date"),
        "skos:definition": _("The date on which the data collection process ended."),
    }

    # Generic date types
    Start = {
        "skos:prefLabel": _("Start Date"),
        "skos:definition": _("The official start date of the project."),
    }

    End = {
        "skos:prefLabel": _("End Date"),
        "skos:definition": _("The official end date of the project."),
    }

    # Dataset date types
    Submitted = {
        "skos:prefLabel": _("Submission Date"),
        "skos:definition": _("The date on which the dataset was submitted for publication."),
    }

    Published = {
        "skos:prefLabel": _("Publication Date"),
        "skos:definition": _("The date on which the dataset was published."),
    }

    Withdrawn = {
        "skos:prefLabel": _("Withdrawal Date"),
        "skos:definition": _("The date on which the dataset was withdrawn from publication."),
    }

    # Sample date types
    Created = {
        "skos:prefLabel": _("Creation date"),
        "skos:definition": _("The date on which the sample was created"),
    }

    Destroyed = {
        "skos:prefLabel": _("Destruction date"),
        "skos:definition": _("The date on which the sample was destroyed"),
    }

    Collected = {
        "skos:prefLabel": _("Collection date"),
        "skos:definition": _("The date on which the sample was collected"),
    }

    Returned = {
        "skos:prefLabel": _("Return date"),
        "skos:definition": _("The date on which the sample was returned"),
    }

    Prepared = {
        "skos:prefLabel": _("Preparation date"),
        "skos:definition": _("The date on which the sample was prepared for analysis"),
    }

    Archival = {
        "skos:prefLabel": _("Storage date"),
        "skos:definition": _("The date on which the sample was stored"),
    }

    Restored = {
        "skos:prefLabel": _("Restoration date"),
        "skos:definition": _("The date on which the sample was restored"),
    }

    # Measurement date types
    Setup = {
        "skos:prefLabel": _("Setup date"),
        "skos:definition": _("The date on which the measurement setup was completed"),
    }

    TearDown = {
        "skos:prefLabel": _("Tear down date"),
        "skos:definition": _("The date on which the measurement teardown was completed"),
    }

    class Meta:
        name = "fairdm-dates"
        prefix = "FAIRDM"
        namespace = "https://www.fairdm.net/vocabularies/"
        scheme_attrs = {
            "skos:prefLabel": _("FairDM Date Types"),
            "skos:definition": _("Important dates regarding archival of metadata related to project management."),
        }
        collections = {
            "Project": Collection(
                prefLabel=_("Project Dates"),
                definition=_("Important dates regarding archival of metadata related to project management."),
                ordered=True,
                members=[
                    "Start",
                    "End",
                ],
            ),
            "Dataset": Collection(
                prefLabel=_("Dataset Dates"),
                definition=_("Important dates regarding archival of metadata related to dataset management."),
                ordered=True,
                members=[
                    "Available",
                    "CollectionStart",
                    "CollectionEnd",
                    "Submitted",
                    "Published",
                    "Withdrawn",
                ],
            ),
            "Sample": Collection(
                prefLabel=_("Sample Dates"),
                definition=_("Important dates regarding archival of metadata related to sample management."),
                ordered=True,
                members=[
                    "Created",
                    "Destroyed",
                    "Collected",
                    "Returned",
                    "Prepared",
                    "Archival",
                    "Restored",
                ],
            ),
            "Measurement": Collection(
                prefLabel=_("Measurement Dates"),
                definition=_("Important dates regarding archival of metadata related to measurement management."),
                ordered=True,
                members=[
                    "Setup",
                    "TearDown",
                ],
            ),
        }


class FairDMRoles(VocabularyBuilder):
    Creator = Concept(
        prefLabel=_("Creator"),
        definition=_("The person or organization responsible for creating the resource."),
    )

    Contributor = Concept(
        prefLabel=_("Contributor"),
        definition=_("A person or organization responsible for making contributions to the resource."),
    )

    Publisher = Concept(
        prefLabel=_("Publisher"),
        definition=_("The person or organization responsible for making the resource available."),
    )

    RightsHolder = Concept(
        prefLabel=_("Rights Holder"),
        definition=_("The person or organization owning the rights to the resource."),
    )

    ContactPerson = Concept(
        prefLabel=_("Contact Person"),
        definition=_("The person to contact for information about the resource."),
    )

    # Dataset roles
    DataCollector = Concept(
        prefLabel=_("Data Collector"),
        definition=_("The person(s) who collected the data."),
    )

    DataCurator = Concept(
        prefLabel=_("Data Curator"),
        definition=_("The person(s) who curated the data."),
    )

    DataManager = Concept(
        prefLabel=_("Data Manager"),
        definition=_("The person(s) who managed the data."),
    )

    Editor = Concept(
        prefLabel=_("Editor"),
        definition=_("The person(s) who edited the data."),
    )

    Producer = Concept(
        prefLabel=_("Producer"),
        definition=_("The person(s) who produced the data."),
    )

    RelatedPerson = Concept(
        prefLabel=_("Related Person"),
        definition=_("A person who is related to the dataset."),
    )

    Researcher = Concept(
        prefLabel=_("Researcher"),
        definition=_("The person(s) who conducted the research."),
    )

    ProjectLeader = Concept(
        prefLabel=_("Project Leader"),
        definition=_("The person(s) who led the project."),
    )

    ProjectManager = Concept(
        prefLabel=_("Project Manager"),
        definition=_("The person(s) who managed the project."),
    )

    ProjectMember = Concept(
        prefLabel=_("Project Member"),
        definition=_("A member of the project."),
    )

    Supervisor = Concept(
        prefLabel=_("Supervisor"),
        definition=_("The person(s) who supervised the project."),
    )

    WorkPackageLeader = Concept(
        prefLabel=_("Work Package Leader"),
        definition=_("The person(s) who led the work package."),
    )

    HostingInstitution = Concept(
        prefLabel=_("Hosting Institution"),
        definition=_("The institution hosting the dataset."),
    )

    ResearchGroup = Concept(
        prefLabel=_("Research Group"),
        definition=_("The research group associated with the dataset."),
    )

    Sponsor = Concept(
        prefLabel=_("Sponsor"),
        definition=_("The sponsor of the project."),
    )

    # Sample roles
    Collection = {
        "skos:prefLabel": _("Collector"),
        "skos:definition": _("The person who collected the sample."),
    }

    Preparation = {
        "skos:prefLabel": _("Preparer"),
        "skos:definition": _("The person who prepared the sample for analysis."),
    }

    Storage = {
        "skos:prefLabel": _("Archivist"),
        "skos:definition": _("The person who stored the sample."),
    }

    Destruction = {
        "skos:prefLabel": _("Destroyer"),
        "skos:definition": _("The person who destroyed the sample."),
    }

    Restoration = {
        "skos:prefLabel": _("Restorer"),
        "skos:definition": _("The person who restored the sample."),
    }

    # Measurement roles
    MeasurementPreparation = Concept(
        prefLabel=_("Preparation"),
        definition=_(
            "Responsible for undertaking procedures and preparations before a measurement is performed, ensuring that all necessary conditions are met for accurate and reliable data acquisition."
        ),
    )

    MeasurementCollection = Concept(
        prefLabel=_("Collection"),
        definition=_(
            "Acquisiton of data or measurements through established methods or protocols, ensuring that the data obtained is comprehensive and representative of the phenomenon being studied."
        ),
    )

    Support = Concept(
        prefLabel=_("Support"),
        definition=_(
            "Provides assistance, guidance, or resources to facilitate the measurement process, ensuring that the necessary tools, equipment, or expertise are available to conduct the measurements effectively."
        ),
    )

    Other = Concept(
        prefLabel=_("Other"),
        definition=_("A role that does not fit into any of the other categories."),
    )

    class Meta:
        name = "fairdm-roles"
        prefix = "FAIRDM"
        namespace = "https://www.fairdm.net/vocabularies/"
        scheme_attrs = {
            "skos:prefLabel": _("FairDM Roles"),
            "skos:definition": _("Roles for the purpose of metadata archival of research projects."),
        }
        collections = {
            "Project": Collection(
                prefLabel=_("Project Roles"),
                definition=_("Roles for the purpose of metadata archival of research projects."),
                ordered=True,
                members=[
                    "Creator",
                    "Contributor",
                    "Publisher",
                    "RightsHolder",
                    "ContactPerson",
                    "Other",
                ],
            ),
            "Dataset": Collection(
                prefLabel=_("Dataset Roles"),
                definition=_("Roles for the purpose of metadata archival of research datasets."),
                ordered=True,
                members=[
                    "Creator",
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
                ],
            ),
            "Sample": Collection(
                prefLabel=_("Sample Roles"),
                definition=_("Roles for the purpose of metadata archival of research samples."),
                ordered=True,
                members=[
                    "Collection",
                    "Preparation",
                    "Storage",
                    "Destruction",
                    "Restoration",
                ],
            ),
            "Measurement": Collection(
                prefLabel=_("Measurement Roles"),
                definition=_("Roles for the purpose of metadata archival of research measurements."),
                ordered=True,
                members=[
                    "MeasurementPreparation",
                    "MeasurementCollection",
                    "Support",
                ],
            ),
        }
