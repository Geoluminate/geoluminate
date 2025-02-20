from django.db import models
from django.utils.translation import gettext_lazy as _
from research_vocabs.builder.skos import Concept
from research_vocabs.registry import vocab_registry
from research_vocabs.vocabularies import VocabularyBuilder

# ================== DATACITE ROLES ==================
# https://support.datacite.org/docs/schema-43-attributes#section-contributor
# https://schema.datacite.org/meta/kernel-4.3/doc/DataCite-MetadataKernel_v4.3.pdf


class CREDiT(VocabularyBuilder):
    """A class for storing choices for CRediT roles on the Contribution model. Based on the
    CRediT Contributor Roles Taxonomy."""

    CONCEPTUALIZATION = Concept(
        prefLabel=_("Conceptualization"),
        definition=_("Ideas; formulation or evolution of overarching research goals and aims."),
    )
    DATA_CURATION = Concept(
        prefLabel=_("Data Curation"), definition=_("Management activities to maintain research data.")
    )
    FORMAL_ANALYSIS = Concept(
        prefLabel=_("Formal Analysis"),
        definition=_(
            "Application of statistical, mathematical, computational, or other formal techniques to analyze or synthesize study data."
        ),
    )
    FUNDING_ACQUISITION = Concept(
        prefLabel=_("Funding Acquisition"),
        definition=_("Obtaining financial support for the project leading to this publication."),
    )
    INVESTIGATION = Concept(
        prefLabel=_("Investigation"), definition=_("Conducting a research and investigation process.")
    )
    METHODOLOGY = Concept(
        prefLabel=_("Methodology"), definition=_("Development or design of methodology; creation of models.")
    )
    PROJECT_ADMINISTRATION = Concept(
        prefLabel=_("Project Administration"),
        definition=_("Management and coordination responsibility for the research activity planning and execution."),
    )
    RESOURCES = Concept(
        prefLabel=_("Resources"),
        definition=_(
            "Provision of study materials, reagents, materials, patients, laboratory samples, animals, instrumentation, computing resources, or other analysis tools."
        ),
    )
    SOFTWARE = Concept(
        prefLabel=_("Software"),
        definition=_(
            "Programming, software development; designing computer programs; implementation of the computer code and supporting algorithms."
        ),
    )
    SUPERVISION = Concept(
        prefLabel=_("Supervision"),
        definition=_(
            "Oversight and leadership responsibility for the research activity planning and execution, including mentorship external to the core team."
        ),
    )
    VALIDATION = Concept(
        prefLabel=_("Validation"),
        definition=_(
            "Verification, whether as a part of the activity or separate, of the overall replication/reproducibility of results/experiments and other research outputs."
        ),
    )
    VISUALIZATION = Concept(
        prefLabel=_("Visualization"),
        definition=_(
            "Preparation, creation and/or presentation of the published work, specifically visualization/data presentation."
        ),
    )
    WRITING_ORIGINAL_DRAFT = Concept(
        prefLabel=_("Writing - Original Draft"),
        definition=_(
            "Preparation, creation and/or presentation of the published work, specifically writing the initial draft (including substantive translation)."
        ),
    )
    WRITING_REVIEW_EDITING = Concept(
        prefLabel=_("Writing - Review & Editing"),
        definition=_(
            "Preparation, creation and/or presentation of the published work by those from the original research group, specifically critical review, commentary or revision."
        ),
    )

    class Meta:
        name = "CRediT"
        prefix = "CRED"
        namespace = "https://credit.niso.org/contributor-roles/"
        scheme_attrs = {
            "skos:prefLabel": _("Contributor Roles"),
        }


vocab_registry.register(CREDiT())


class PersonalIdentifiers(models.TextChoices):
    ORCID = "ORCID", "ORCID"
    RESEARCHER_ID = "ResearcherID", "ResearcherID"


class OrganizationalIdentifiers(models.TextChoices):
    ROR = "ROR", "ROR"
    GRID = "GRID", "GRID"
    WIKIDATA = "Wikidata", "Wikidata"
    ISNI = "ISNI", "ISNI"
    CROSSREF_FUNDER_ID = "Crossref Funder ID", "Crossref Funder ID"


class FairDMIdentifiers(VocabularyBuilder):
    ORCID = Concept(
        prefLabel=_("ORCID"),
        definition=_("Open Researcher and Contributor ID."),
    )


IdentifierLookup = {
    "ORCID": "https://orcid.org/",
    "ROR": "https://ror.org/",
    "GRID": "https://www.grid.ac/institutes/",
    "Wikidata": "https://www.wikidata.org/wiki/",
    "ISNI": "https://isni.org/isni/",
    "Crossref Funder ID": "https://doi.org/",
}
