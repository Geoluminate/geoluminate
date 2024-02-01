from django.db import models
from django.utils.translation import gettext_lazy as _


class DataCiteDateTypes(models.TextChoices):
    """DataCite date types as per https://schema.datacite.org/meta/kernel-4.4/doc/DataCite-MetadataKernel_v4.4.pdf#page=46"""

    ACCEPTED = "Accepted", _("Accepted")
    AVAILABLE = "Available", _("Available")
    COPYRIGHTED = "Copyrighted", _("Copyright")
    COLLECTED = "Collected", _("Collected")
    CREATED = "Created", _("Created")
    ISSUED = "Issued", _("Issued")
    SUBMITTED = "Submitted", _("Submitted")
    UPDATED = "Updated", _("Updated")
    VALID = "Valid", _("Valid")
    WITHDRAWN = "Withdrawn", _("Withdrawn")


class DataCiteRelationTypes(models.TextChoices):
    """DataCite relation types as per https://schema.datacite.org/meta/kernel-4.4/doc/DataCite-MetadataKernel_v4.4.pdf#page=58"""

    IsCitedBy = "IsCitedBy", _("Is Cited By")
    Cites = "Cites", _("Cites")
    IsSupplementTo = "IsSupplementTo", _("Is Supplement To")
    IsSupplementedBy = "IsSupplementedBy", _("Is Supplemented By")
    IsContinuedBy = "IsContinuedBy", _("Is Continued By")
    Continues = "Continues", _("Continues")
    Describes = "Describes", _("Describes")
    IsDescribedBy = "IsDescribedBy", _("Is Described By")
    HasMetadata = "HasMetadata", _("Has Metadata")
    IsMetadataFor = "IsMetadataFor", _("Is Metadata For")
    HasVersion = "HasVersion", _("Has Version")
    IsVersionOf = "IsVersionOf", _("Is Version Of")
    IsNewVersionOf = "IsNewVersionOf", _("Is New Version Of")
    IsPreviousVersionOf = "IsPreviousVersionOf", _("Is Previous Version Of")
    IsPartOf = "IsPartOf", _("Is Part Of")
    HasPart = "HasPart", _("Has Part")
    IsPublishedIn = "IsPublishedIn", _("Is Published In")
    IsReferencedBy = "IsReferencedBy", _("Is Referenced By")
    References = "References", _("References")
    IsDocumentedBy = "IsDocumentedBy", _("Is Documented By")
    Documents = "Documents", _("Documents")
    IsCompiledBy = "IsCompiledBy", _("Is Compiled By")
    Compiles = "Compiles", _("Compiles")
    IsVariantFormOf = "IsVariantFormOf", _("Is Variant Form Of")
    IsOriginalFormOf = "IsOriginalFormOf", _("Is Original Form Of")
    IsIdenticalTo = "IsIdenticalTo", _("Is Identical To")
    IsReviewedBy = "IsReviewedBy", _("Is Reviewed By")
    Reviews = "Reviews", _("Reviews")
    IsDerivedFrom = "IsDerivedFrom", _("Is Derived From")
    IsSourceOf = "IsSourceOf", _("Is Source Of")
    IsRequiredBy = "IsRequiredBy", _("Is Required By")
    Requires = "Requires", _("Requires")
    Obsoletes = "Obsoletes", _("Obsoletes")
    IsObsoletedBy = "IsObsoletedBy", _("Is Obsoleted By")


class DataCiteDescriptionTypes(models.TextChoices):
    """DataCite description types as per https://schema.datacite.org/meta/kernel-4.4/doc/DataCite-MetadataKernel_v4.4.pdf#page=65"""

    ABSTRACT = "Abstract", _("Abstract")
    METHODS = "Methods", _("Methods")
    SERIES_INFORMATION = "SeriesInformation", _("Series Information")
    TABLE_OF_CONTENTS = "TableOfContents", _("Table of Contents")
    TECHNICAL_INFO = "TechnicalInfo", _("Technical Information")
    OTHER = "Other", _("Other")
    EXP = "ExpectedOutput", _("Expected Output")


class DataCiteIdentifiers(models.TextChoices):
    """DataCite identifier types as per https://schema.datacite.org/meta/kernel-4.4/doc/DataCite-MetadataKernel_v4.4.pdf#page=54"""

    ARK = "ARK", "ARK"
    ARXIV = "arXiv", "arXiv"
    BIBCODE = "bibcode", "bibcode"
    DOI = "DOI", "DOI"
    EAN13 = "EAN13", "EAN13"
    EISSN = "EISSN", "EISSN"
    HANDLE = "Handle", "Handle"
    IGSN = "IGSN", "IGSN"
    ISBN = "ISBN", "ISBN"
    ISSN = "ISSN", "ISSN"
    ISTC = "ISTC", "ISTC"
    LISSN = "LISSN", "LISSN"
    LSID = "LSID", "LSID"
    PMID = "PMID", "PMID"
    PURL = "PURL", "PURL"
    UPC = "UPC", "UPC"
    URL = "URL", "URL"
    URN = "URN", "URN"
