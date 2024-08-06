from django.utils.translation import gettext as _
from research_vocabs.builder.skos import Concept
from research_vocabs.vocabularies import VocabularyBuilder


class MeasurementDescriptions(VocabularyBuilder):
    """A class for storing choices for the descriptions of a measurement on the Sample model."""

    Conditions = Concept(
        prefLabel=_("Conditions"),
        definition=_(
            "The specific environmental or situational factors present during the measurement process, which can influence or affect the outcome."
        ),
    )
    Preparation = Concept(
        prefLabel=_("Preparation"),
        definition=_(
            "The set of procedures and steps executed prior to conducting a measurement, ensuring accuracy, reliability, and consistency in the results obtained."
        ),
    )
    Other = Concept(
        prefLabel=_("Other"),
        definition=_(
            "Any additional relevant information or miscellaneous details not covered by existing description types, which may be significant for understanding or interpreting the measurements."
        ),
    )

    class Meta:
        name = "measurement-descriptions"
        prefix = "GEOL"
        namespace = "https://www.geoluminate.net/vocabularies/"
        scheme_attrs = {
            "skos:prefLabel": _("Dataset Description Types"),
            "skos:definition": _("Description types for the purpose of metadata archival of datasets."),
        }


class MeasurementDates(VocabularyBuilder):
    """A class for storing choices for the dates of a measurement on the Sample model."""

    StartDate = Concept(
        prefLabel=_("Start Date"),
        definition=_("The date when the measurement process commenced."),
    )

    EndDate = Concept(
        prefLabel=_("End Date"),
        definition=_("The date when the measurement process concluded."),
    )

    CollectionDate = Concept(
        prefLabel=_("Collection Date"),
        definition=_("The date when the sample was collected for measurement."),
    )

    class Meta:
        name = "measurement-dates"
        prefix = "GEOL"
        namespace = "https://www.geoluminate.net/vocabularies/"
        scheme_attrs = {
            "skos:prefLabel": _("Dataset Description Types"),
            "skos:definition": _("Description types for the purpose of metadata archival of datasets."),
        }


class MeasurementRoles(VocabularyBuilder):
    """A class for storing choices for the roles of a measurement on the Sample model."""

    Preparation = Concept(
        prefLabel=_("Preparation"),
        definition=_(
            "Responsible for undertaking procedures and preparations before a measurement is performed, ensuring that all necessary conditions are met for accurate and reliable data acquisition."
        ),
    )

    Collection = Concept(
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
        definition=_(
            "Any additional roles or responsibilities not covered by existing role types, which may be relevant to the measurement process or contribute to the overall success of the project."
        ),
    )

    class Meta:
        name = "measurement-roles"
        prefix = "GEOL"
        namespace = "https://www.geoluminate.net/vocabularies/"
        scheme_attrs = {
            "skos:prefLabel": _("Dataset Description Types"),
            "skos:definition": _("Description types for the purpose of metadata archival of datasets."),
        }
