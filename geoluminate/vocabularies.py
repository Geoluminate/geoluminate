from django.utils.translation import gettext_lazy as _
from rdflib import RDF, SKOS, Graph, Namespace
from research_vocabs.concepts import ConceptSchemeBuilder


class ProjectDiscoveryTags(ConceptSchemeBuilder):

    LookingForCollaborators = {
        SKOS.prefLabel: _("Looking for collaborators"),
        SKOS.definition: _("This project is actively looking for collaborators to help with the research."),
    }
    LookingForFunding = {
        SKOS.prefLabel: _("Looking for funding"),
        SKOS.definition: _("This project is actively looking for funding to support the research."),
    }

    LookingForInstrumentation = {
        SKOS.prefLabel: _("Looking for instrumentation"),
        SKOS.definition: _("This project is actively looking for scientific instrumentation to support the research."),
    }

    # class Meta:
