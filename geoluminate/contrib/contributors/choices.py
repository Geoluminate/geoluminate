from django.db import models
from django.utils.translation import gettext_lazy as _
from research_vocabs.vocabularies import VocabularyBuilder

# ================== DATACITE ROLES ==================
# https://support.datacite.org/docs/schema-43-attributes#section-contributor
# https://schema.datacite.org/meta/kernel-4.3/doc/DataCite-MetadataKernel_v4.3.pdf


class CREDiT(VocabularyBuilder):
    """A class for storing choices for CRediT roles on the Contribution model. Based on the
    CRediT Contributor Roles Taxonomy."""

    CONCEPTUALIZATION = {
        "skos:prefLabel": _("Conceptualization"),
        "SKOS.definition": _("Ideas; formulation or evolution of overarching research goals and aims."),
    }
    DATA_CURATION = {
        "skos:prefLabel": _("Data Curation"),
        "SKOS.definition": _("Management activities to maintain research data."),
    }
    FORMAL_ANALYSIS = {
        "skos:prefLabel": _("Formal Analysis"),
        "SKOS.definition": _(
            "Application of statistical, mathematical, computational, or other formal techniques to analyze or synthesize study data."
        ),
    }
    FUNDING_ACQUISITION = {
        "skos:prefLabel": _("Funding Acquisition"),
        "SKOS.definition": _("Obtaining financial support for the project leading to this publication."),
    }
    INVESTIGATION = {
        "skos:prefLabel": _("Investigation"),
        "SKOS.definition": _("Conducting a research and investigation process."),
    }
    METHODOLOGY = {
        "skos:prefLabel": _("Methodology"),
        "SKOS.definition": _("Development or design of methodology; creation of models."),
    }
    PROJECT_ADMINISTRATION = {
        "skos:prefLabel": _("Project Administration"),
        "SKOS.definition": _(
            "Management and coordination responsibility for the research activity planning and execution."
        ),
    }
    RESOURCES = {
        "skos:prefLabel": _("Resources"),
        "SKOS.definition": _(
            "Provision of study materials, reagents, materials, patients, laboratory samples, animals, instrumentation, computing resources, or other analysis tools."
        ),
    }
    SOFTWARE = {
        "skos:prefLabel": _("Software"),
        "SKOS.definition": _(
            "Programming, software development; designing computer programs; implementation of the computer code and supporting algorithms."
        ),
    }
    SUPERVISION = {
        "skos:prefLabel": _("Supervision"),
        "SKOS.definition": _(
            "Oversight and leadership responsibility for the research activity planning and execution, including mentorship external to the core team."
        ),
    }
    VALIDATION = {
        "skos:prefLabel": _("Validation"),
        "SKOS.definition": _(
            "Verification, whether as a part of the activity or separate, of the overall replication/reproducibility of results/experiments and other research outputs."
        ),
    }
    VISUALIZATION = {
        "skos:prefLabel": _("Visualization"),
        "SKOS.definition": _(
            "Preparation, creation and/or presentation of the published work, specifically visualization/data presentation."
        ),
    }
    WRITING_ORIGINAL_DRAFT = {
        "skos:prefLabel": _("Writing - Original Draft"),
        "SKOS.definition": _(
            "Preparation, creation and/or presentation of the published work, specifically writing the initial draft (including substantive translation)."
        ),
    }
    WRITING_REVIEW_EDITING = {
        "skos:prefLabel": _("Writing - Review & Editing"),
        "SKOS.definition": _(
            "Preparation, creation and/or presentation of the published work by those from the original research group, specifically critical review, commentary or revision."
        ),
    }

    class Meta:
        # namespace = "https://credit.niso.org/contributor-roles/"
        # namespace_prefix = "CREDiT"
        scheme_attrs = {
            "skos:prefLabel": _("Contributor Roles"),
        }


class PersonalIdentifiers(models.TextChoices):
    ORCID = "https://orcid.org/", "ORCID"
    RESEARCHER_ID = "ResearcherID", "ResearcherID"


class OrganizationalIdentifiers(models.TextChoices):
    ROR = "ROR", "ROR"
    GRID = "GRID", "GRID"
    WIKIDATA = "Wikidata", "Wikidata"
    ISNI = "ISNI", "ISNI"
    CROSSREF_FUNDER_ID = "Crossref Funder ID", "Crossref Funder ID"


IdentifierLookup = {
    "ORCID": "https://orcid.org/",
    "ROR": "https://ror.org/",
    "GRID": "https://www.grid.ac/institutes/",
    "Wikidata": "https://www.wikidata.org/wiki/",
    "ISNI": "https://isni.org/isni/",
    "Crossref Funder ID": "https://doi.org/",
}
