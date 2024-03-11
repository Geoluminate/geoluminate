from django.utils.translation import gettext as _
from research_vocabs.concepts import ConceptSchemeBuilder, LocalConceptScheme


class FeatureType(LocalConceptScheme):
    class Meta:
        source = "samplingfeaturetype.rdf"


class SamplingMedium(LocalConceptScheme):
    class Meta:
        source = "medium.rdf"


class SampleStatus(LocalConceptScheme):
    class Meta:
        source = "status.rdf"


class SpecimenType(LocalConceptScheme):
    class Meta:
        source = "specimentype.rdf"


class DescriptionTypes(ConceptSchemeBuilder):
    Preparation = {
        "SKOS.prefLabel": _("Preparation"),
        "SKOS.definition": _("The process of preparing a sample for analysis."),
    }

    class Meta:
        namespace = "https://www.heatflow.world/vocabularies/"
        namespace_prefix = "GEOLUM"
        conceptscheme = {
            "SKOS.prefLabel": _("Sample Description Types"),
            "SKOS.hasTopConcept": [
                "Preparation",
            ],
        }
        collections = {
            "Sample": ["Preparation"],
        }


DescriptionTypes.as_collection("Sample")

# print(list(DescriptionTypes.choices))
