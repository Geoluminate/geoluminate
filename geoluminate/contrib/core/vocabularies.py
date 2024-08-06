from django.utils.translation import gettext_lazy as _
from research_vocabs.builder.skos import Collection, Concept
from research_vocabs.vocabularies import VocabularyBuilder


class GeoluminateDescriptions(VocabularyBuilder):
    Abstract = Concept(
        prefLabel=_("Abstract"),
        definition=_(
            "A concise summary of a larger work, highlighting main points that allow a reader to quickly understand the essence of the work without reading the entire document."
        ),
    )

    Collection = Concept(
        prefLabel=_("Collection"),
        definition=_("The process of collecting a sample."),
    )

    Preparation = Concept(
        prefLabel=_("Preparation"),
        definition=_("The process of preparing a sample for analysis."),
    )

    Storage = Concept(
        prefLabel=_("Storage"),
        definition=_("The process of storing a sample."),
    )

    Destruction = Concept(
        prefLabel=_("Destruction"),
        definition=_("The process of destroying a sample."),
    )

    Comment = Concept(
        prefLabel=_("Comment"),
        definition=_("A general comment about the sample."),
    )

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
        name = "description-types"
        prefix = "GEOL"
        namespace = "https://www.geoluminate.net/vocabularies/"
        scheme_attrs = {
            "skos:prefLabel": _("Description Types"),
            "skos:definition": _("Description types for the purpose of metadata archival."),
        }

        collections = {
            "project-descriptions": Collection(
                prefLabel=_("Project Description Types"),
                definition=_("Description types for the purpose of metadata archival of research projects."),
                members=["Abstract"],
                ordered=True,
            ),
            "dataset-descriptions": Collection(
                prefLabel=_("Dataset Description Types"),
                definition=_("Description types for the purpose of metadata archival of datasets."),
                members=["Abstract"],
                ordered=True,
            ),
            "sample-descriptions": Collection(
                prefLabel=_("Sample Description Types"),
                definition=_("Description types for the purpose of metadata archival of samples."),
                members=["Collection", "Preparation", "Storage", "Destruction", "Comment"],
                ordered=True,
            ),
            "measurement-descriptions": Collection(
                prefLabel=_("Measurement Description Types"),
                definition=_("Description types for the purpose of metadata archival of measurements."),
                members=["Conditions", "Preparation", "Other"],
                ordered=True,
            ),
        }


class GeoluminateDates(VocabularyBuilder):
    StartDate = Concept(
        prefLabel=_("Start Date"),
        definition=_("The date on which data collection commenced"),
    )

    EndDate = Concept(
        prefLabel=_("End Date"),
        definition=_("The date on which data collected stopped."),
    )

    CollectionStart = Concept(
        prefLabel=_("Collection start"),
        definition=_("The date on which the collection process for the sample started"),
    )

    CollectionFinish = Concept(
        prefLabel=_("Collection finish"),
        definition=_("The date on which the collection process for the sample finished"),
    )

    CollectionDate = Concept(
        prefLabel=_("Collection date"),
        definition=_("The date on which the sample was collected"),
    )

    class Meta:
        name = "date-types"
        prefix = "GEOL"
        namespace = "https://www.geoluminate.net/vocabularies/"
        scheme_attrs = {
            "skos:prefLabel": _("Geoluminate Date Types"),
            "skos:definition": _("Important dates regarding archival of metadata related to project management."),
        }

        collections = {
            "project-dates": Collection(
                prefLabel=_("Project Description Types"),
                definition=_("Description types for the purpose of metadata archival of research projects."),
                ordered=True,
                members=["StartDate", "EndDate"],
            ),
            "dataset-dates": Collection(
                prefLabel=_("Dataset Date Types"),
                definition=_("Important dates regarding dataset management and metadata archival"),
                ordered=True,
                members=["StartDate", "EndDate"],
            ),
            "sample-dates": Collection(
                prefLabel=_("Sample Date Types"),
                definition=_("Important dates regarding archival of metadata related to generic sample collection."),
                ordered=True,
                members=["CollectionStart", "CollectionFinish", "CollectionDate"],
            ),
            "measurement-dates": Collection(
                prefLabel=_("Measurement Date Types"),
                definition=_("Important dates regarding archival of metadata related to measurements."),
                ordered=True,
                members=["StartDate", "EndDate", "CollectionDate"],
            ),
        }


class GeoluminateRoles(VocabularyBuilder):
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
            "Any additional relevant information or miscellaneous details not covered by existing description types, which may be significant for understanding or interpreting the measurements."
        ),
    )

    class Meta:
        name = "contributor-roles"
        prefix = "GEOL"
        namespace = "https://www.geoluminate.net/vocabularies/"
        scheme_attrs = {
            "skos:prefLabel": _("Geoluminate Role Types"),
            "skos:definition": _("Roles associated with the measurement process."),
        }

        collections = {
            "measurement-roles": Collection(
                prefLabel=_("Measurement Role Types"),
                definition=_("Roles associated with the measurement process."),
                ordered=True,
                members=["Preparation", "Collection", "Support"],
            ),
        }
