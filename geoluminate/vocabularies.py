from django.utils.translation import gettext_lazy as _
from research_vocabs.vocabularies import VocabularyBuilder


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
