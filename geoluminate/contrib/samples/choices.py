from django.db import models
from django.utils.translation import gettext as _
from research_vocabs.vocabularies import LocalVocabulary, VocabularyBuilder


class FeatureType(LocalVocabulary):
    class Meta:
        source = "./vocab_data/samplingfeaturetype.rdf"
        prefix = "odm2b"
        namespace = "http://vocabulary.odm2.org/samplingfeaturetype/"


# http://vocabulary.odm2.org/api/v1/actiontype/?format=skos


class SamplingMedium(LocalVocabulary):
    class Meta:
        source = "./vocab_data/medium.rdf"
        namespace = "http://vocabulary.odm2.org/medium/"
        prefix = "odm2"


class SampleStatus(LocalVocabulary):
    class Meta:
        source = "./vocab_data/status.rdf"
        prefix = "odm2"
        namespace = "http://vocabulary.odm2.org/status/"


class SpecimenType(LocalVocabulary):
    class Meta:
        source = "./vocab_data/specimentype.rdf"
        prefix = "odm2"
        namespace = "http://vocabulary.odm2.org/specimentype/"


class SampleDescriptions(VocabularyBuilder):
    Collection = {
        "skos:prefLabel": _("Collection"),
        "skos:definition": _("The process of collecting a sample."),
    }
    Preparation = {
        "skos:prefLabel": _("Preparation"),
        "skos:definition": _("The process of preparing a sample for analysis."),
    }
    Storage = {
        "skos:prefLabel": _("Storage"),
        "skos:definition": _("The process of storing a sample."),
    }
    Destruction = {
        "skos:prefLabel": _("Destruction"),
        "skos:definition": _("The process of destroying a sample."),
    }
    Comment = {
        "skos:prefLabel": _("Comment"),
        "skos:definition": _("A general comment about the sample."),
    }

    class Meta:
        name = "sample-descriptions"
        namespace = "https://www.geoluminate.net/vocabularies/"
        prefix = "GEOL"
        scheme_attrs = {
            "skos:prefLabel": _("Sample Description Types"),
        }


class SampleDates(VocabularyBuilder):
    CollectionStart = {
        "skos:prefLabel": _("Collection start"),
        "skos:definition": _("The date on which the collection process for the sample started"),
    }
    CollectionFinish = {
        "skos:prefLabel": _("Collection finish"),
        "skos:definition": _("The date on which the collection process for the sample finished"),
    }
    CollectionDate = {
        "skos:prefLabel": _("Collection date"),
        "skos:definition": _("The date on which the sample was collected"),
    }

    class Meta:
        name = "sample-dates"
        prefix = "GEOL"
        namespace = "https://www.geoluminate.net/vocabularies/"
        scheme_attrs = {
            "skos:prefLabel": _("Sample Date Types"),
            "skos:definition": _(
                "Important dates regarding archival of metadata related to generic sample collection."
            ),
        }


class SampleRoles(models.TextChoices):
    """A class for storing"""

    COLLECTION = "Collection", _("Collection")
    PREPARATION = "Preparation", _("Preparation")
    STORAGE = "Storage", _("Storage")
    DESTRUCTION = "Destruction", _("Destruction")
